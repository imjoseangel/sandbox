import logging
import os
import sys
from typing import Any, List

import gradio as gr

import pymongo

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import QueryEngineTool, BaseTool
from llama_index.core.agent import ReActAgent
from llama_index.core.settings import Settings
from llama_index.core.base.agent.types import StreamingAgentChatResponse


# --- Configuration & Initialization ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Initialize Gemini LLM & Embeddings
Settings.llm = Gemini(api_key=os.getenv("GEMINI_API_KEY"),
                      model_name="models/gemini-1.5-flash-latest")  # Changed to a standard model name
Settings.embed_model = GeminiEmbedding(api_key=os.getenv(
    "GEMINI_API_KEY"), model_name="models/text-embedding-004")

# Initialize MongoDB Atlas
# --- Configuration ---
MONGO_PASSWORD = os.getenv("MONGODB_PASSWORD")
if not MONGO_PASSWORD:
    logging.error(
        "Error: MONGODB_PASSWORD environment variable not set.")
    sys.exit(1)

MONGO_DB = "XX"
MONGO_HOST = "xx.hgmrw.mongodb.net"
MONGO_CONNECTION_STRING = f"mongodb+srv://{MONGO_DB}:{MONGO_PASSWORD}@{MONGO_HOST}/"
os.environ["MONGODB_URI"] = MONGO_CONNECTION_STRING
MONGO_COLLECTION = "vector_collection"
MONGO_VECTORINDEX = "vector_index"

mongo_client: pymongo.MongoClient = pymongo.MongoClient(
    MONGO_CONNECTION_STRING)
db_name = MONGO_DB
collection_name = MONGO_COLLECTION
index_name = MONGO_VECTORINDEX

vector_store = MongoDBAtlasVectorSearch(
    client=mongo_client,
    db_name=db_name,
    collection_name=collection_name,
    index_name=index_name,
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# --- Global Variables ---
agent = None  # Will be initialized later

# --- RAG Query Engine ---


def get_rag_query_engine():
    return VectorStoreIndex.from_vector_store(
        vector_store=vector_store
    ).as_query_engine(
        similarity_top_k=3,
        response_mode="compact",
        streaming=False  # Tool expects a single response, not a stream
    )

# --- Custom Robust RAG Tool ---


class RobustQueryEngineTool(QueryEngineTool):
    async def _acall(self, **kwargs: Any) -> str:
        query_str = kwargs.get("input", "")
        if not isinstance(query_str, str) or not query_str.strip():
            logging.warning(
                f"RobustQueryEngineTool received invalid input: {kwargs}")
            return "Error: Invalid or empty query provided to the document retriever."

        try:
            # type: LlamaResponse
            response_obj = await self._query_engine.aquery(query_str)

            actual_response_str = getattr(response_obj, 'response', None)

            if actual_response_str is None or actual_response_str.strip() == "":
                num_source_nodes = len(response_obj.source_nodes) if response_obj and hasattr(
                    response_obj, 'source_nodes') else 0
                logging.info(
                    f"RAG query for '{query_str}' yielded no text response. "
                    f"Source nodes found: {num_source_nodes}")
                if num_source_nodes == 0:
                    return ("No relevant documents were found in the knowledge "
                            "base to answer the query.")
                else:
                    return ("Relevant documents were found, but no direct "
                            "answer could be synthesized from them.")
            return actual_response_str
        except Exception as e:
            logging.error(
                f"Error during RobustQueryEngineTool._acall for query "
                f"'{query_str}': {e}", exc_info=True)
            return f"An error occurred while trying to retrieve documents: {str(e)}"


# --- Import Tools ---
# Make sure tools directory and files exist as previously described

# --- Agent Initialization ---

def initialize_agent():
    global agent
    actions_log = ["Initializing Agent..."]
    try:
        rag_query_engine = get_rag_query_engine()
        # Use the RobustQueryEngineTool
        knowledge_base_tool = RobustQueryEngineTool.from_defaults(
            query_engine=rag_query_engine,
            name="knowledge_base_retriever",
            description=(
                "Use this tool to retrieve specific information, definitions, explanations, "
                "best practices, and other contextual details from uploaded documents in the "
                "MongoDB Atlas knowledge base. "
                "For example, ask 'What is the formula for X?' or 'Explain Y best practices.'"
            )
        )
        tools_for_agent: List[BaseTool] = [knowledge_base_tool]
        chat_memory = ChatMemoryBuffer.from_defaults(token_limit=3500)

        agent = ReActAgent.from_tools(
            tools=tools_for_agent,
            llm=Settings.llm,
            memory=chat_memory,
            verbose=True,  # Logs thoughts to console, helpful for debugging
            # LlamaIndex ReActAgent supports streaming out-of-the-box with astream_chat
        )
        actions_log.append(
            "Agent initialized successfully with Knowledge Base Retriever tool.")
        logging.info("Agent initialized.")
    except Exception as e:
        error_msg = f"Error initializing agent: {e}"
        actions_log.append(error_msg)
        logging.error(error_msg, exc_info=True)
    return "\n".join(actions_log)


# --- Call initializations ---
initialization_logs = initialize_agent()

# --- Gradio Chat Interface Logic (with Streaming) ---
# Adapted for gr.ChatInterface


async def chat_bot_logic(message: str | None,
                         # [[user, bot], [user, bot], ...]
                         history_list_of_lists: list,
                         session_state: dict,
                         current_actions_log_content: str):
    global agent

    # Ensure current_actions_log_content is initialized if None (should not happen with value set)
    if current_actions_log_content is None:
        current_actions_log_content = initialization_logs
    elif not isinstance(current_actions_log_content, str):  # Ensure it's a string
        current_actions_log_content = str(current_actions_log_content)

    turn_specific_log_entries = []

    if not agent:
        error_msg = "ERROR: Agent not initialized. Chat interface cannot function."
        turn_specific_log_entries.append(error_msg)
        logging.error(error_msg)
        if message:  # Only yield error if there was a user message trying to be processed
            yield "Agent is not ready. Please check the application logs."
        new_full_log = current_actions_log_content + "\n\n" + \
            "\n".join(
                turn_specific_log_entries)  # Added extra newline for spacing
        yield "", session_state, new_full_log  # Yield empty chat string, state, and log
        return

    # Handle "Clear" button click (message is None from gr.ChatInterface clear_btn)
    if message is None:
        agent.reset()
        turn_specific_log_entries.append(
            "SYSTEM: New conversation started by button. Memory has been cleared.")
        logging.info(
            "New conversation started via clear button (message is None).")
        session_state["chat_history"] = []  # Reset our state's history tracker
        # No chat message to yield. gr.ChatInterface handles clearing the chat display.
        new_full_log = current_actions_log_content + \
            "\n\n" + "\n".join(turn_specific_log_entries)
        # Yield empty chat string, state, and log for additional_outputs
        yield "", session_state, new_full_log
        return

    # Handle user message
    turn_specific_log_entries.append(f"User: {message}")
    turn_specific_log_entries.append("Chatbot thinking...")

    # Handle "new conversation" text command (optional, clear_btn is primary)
    if message.lower().strip() == "new conversation":
        agent.reset()
        bot_response = "Okay, I've started a new conversation. How can I help you?"
        turn_specific_log_entries.append(
            "SYSTEM: New conversation started by text command. Memory has been cleared.")
        logging.info(
            "New conversation started by user input 'new conversation'.")
        session_state["chat_history"] = []  # Reset our state's history tracker
        yield bot_response  # Stream bot response
        new_full_log = current_actions_log_content + \
            "\n\n" + "\n".join(turn_specific_log_entries)
        # Yield final chat, state, and log
        yield bot_response, session_state, new_full_log
        return

    try:
        response_payload = await agent.astream_chat(message)
        full_response_text = ""
        final_stream_sources = []

        if not isinstance(response_payload, StreamingAgentChatResponse):
            error_detail = (f"Unexpected response type from agent: {type(response_payload)}. "
                            f"Expected StreamingAgentChatResponse.")
            turn_specific_log_entries.append(f"ERROR: {error_detail}")
            logging.error(error_detail)
            full_response_text = "Error: Could not process agent response due to unexpected type."
            yield full_response_text  # Stream error to chat
            new_full_log = current_actions_log_content + \
                "\n\n" + "\n".join(turn_specific_log_entries)
            # Yield final chat, state, and log
            yield full_response_text, session_state, new_full_log
            return

        logging.info(
            "Received StreamingAgentChatResponse object. Processing stream...")
        turn_specific_log_entries.append(
            "INFO: Processing agent response stream...")

        async for text_token in response_payload.async_response_gen():
            if text_token:
                full_response_text += text_token
                yield full_response_text  # Stream to gr.ChatInterface

        if not full_response_text:
            response_obj = getattr(response_payload, 'response', None)
            if response_obj:
                actual_response_str = getattr(response_obj, 'response', None)
                if actual_response_str:
                    logging.info(
                        "Stream yielded no text, using fallback from "
                        "response_payload.response.response.")
                    full_response_text = actual_response_str
                    yield full_response_text  # Yield the fallback

        if hasattr(response_payload, 'sources') and response_payload.sources:
            final_stream_sources = response_payload.sources
            logging.info(
                f"Found {len(final_stream_sources)} sources after streaming.")

        turn_specific_log_entries.append(f"Chatbot: {full_response_text}")

        if final_stream_sources:
            turn_specific_log_entries.append("ACTIONS & SOURCES:")
            for i, tool_output_source in enumerate(final_stream_sources):
                tool_name = tool_output_source.tool_name
                raw_input_str = str(
                    getattr(tool_output_source, 'raw_input', 'N/A'))[:200]
                raw_output_str = str(
                    getattr(tool_output_source, 'raw_output', 'N/A'))[:200]
                turn_specific_log_entries.append(
                    f"  Source {i+1}: Tool Used: '{tool_name}'\n"
                    f"    Input: {raw_input_str}{'...' if len(str(getattr(tool_output_source, 'raw_input', ''))) > 200 else ''}\n"
                    f"    Output: {raw_output_str}{'...' if len(str(getattr(tool_output_source, 'raw_output', ''))) > 200 else ''}\n"
                )
        else:
            turn_specific_log_entries.append(
                "No explicit tool sources reported by the agent for this interaction.")

        # Update our state tracker
        session_state["chat_history"] = history_list_of_lists
        new_full_log = current_actions_log_content + "\n\n" + \
            "\n".join(turn_specific_log_entries)  # Added extra newline
        # Yield final chat, state, and log
        yield full_response_text, session_state, new_full_log
        return

    except Exception as e:
        error_msg = f"Sorry, an error occurred: {str(e)}"
        logging.error(f"Error during chat stream: {e}", exc_info=True)
        turn_specific_log_entries.append(f"ERROR processing your request: {e}")
        yield error_msg  # Stream error to chat
        new_full_log = current_actions_log_content + \
            "\n\n" + "\n".join(turn_specific_log_entries)
        yield error_msg, session_state, new_full_log  # Yield final chat, state, and log
        return

# --- Gradio Interface Definition ---
with gr.Blocks(theme=gr.themes.Citrus(primary_hue="blue"),
               title="MongoDB Chatbot Expert") as demo:
    gr.HTML("""
    <style>
        body {
            background: #f8fafc;
        }
        .gradio-container {
            font-family: 'Segoe UI', 'Roboto', sans-serif;
        }
        .chatbot-avatar-user {
            border-radius: 50%;
            border: 2px solid #d1eaff;
            background: #e3f1ff;
            width: 42px;
            height: 42px;
            object-fit: cover;
            margin: 0 6px 0 0;
        }
        .chatbot-avatar-bot {
            border-radius: 50%;
            border: 2px solid #ffd580;
            background: #fff8e1;
            width: 42px;
            height: 42px;
            object-fit: cover;
            margin: 0 0 0 6px;
        }
        .chatbot-message-user {
            background: linear-gradient(90deg, #e3f1ff 0%, #c9e7ff 100%);
            color: #222;
        }
        .chatbot-message-bot {
            background: linear-gradient(90deg, #fff8e1 0%, #fff3c4 100%);
        }
        .actions-log {
            font-family: monospace;
            font-size: 13px;
            background: #f4f4f5;
            border-radius: 12px;
            padding: 12px;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
            height: 520px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
        .header-container {
            position: sticky;
            top: 0;
            background: #ffffff;
            z-index: 10;
            padding-bottom: 8px;
        }
    </style>
    """)

    with gr.Column(elem_id="header", elem_classes="header-container"):
        gr.Markdown("""
        # 🧑🏻‍💻 MongoDB Chatbot Expert 🤖

        ## Welcome to your MongoDB assistant. Ask away!

        - 📄 **Knowledge Base**: Tips, facts, and business insights.
        - 🧠 **Context-Aware**: Handles ongoing conversations.
        - 🔁 **Reset Session** to start from scratch.
        - 📝 **Actions Log**: Real-time backend visibility.
        """)

    # session_state for agent's memory and other potential state variables
    session_data_state = gr.State(value={"chat_history": []})

    with gr.Row():
        with gr.Column(scale=3):
            actions_taken_display_ref = gr.Textbox(visible=False)

            chat_ui = gr.ChatInterface(
                fn=chat_bot_logic,
                additional_inputs=[session_data_state,
                                   actions_taken_display_ref],

                chatbot=gr.Chatbot(
                    label="Conversation",
                    bubble_full_width=True,
                    avatar_images=(
                        "https://img.icons8.com/fluency/96/user-female-circle.png",
                        "https://img.icons8.com/fluency/96/chatbot.png"),
                    height=700,
                    show_label=True,
                    render_markdown=True,
                    autoscroll=True
                ),
            )
        with gr.Column(scale=1):
            gr.Markdown("## 📝 Actions Log")
            actions_taken_display = gr.Textbox(
                label="Chatbot Actions & System Logs",
                lines=30,
                interactive=False,
                max_lines=40,
                value=initialization_logs
            )

    chat_ui.additional_inputs = [session_data_state, actions_taken_display]
    chat_ui.additional_outputs = [session_data_state, actions_taken_display]


if __name__ == "__main__":
    logging.info("Starting Gradio app with streaming support...")
    print("Initialization logs (also in UI on startup):\n", initialization_logs)
    print("Finance Chatbot Expert is starting. Access it at the URL provided by Gradio.")
    # .queue() is important for handling multiple users/requests and streaming
    demo.queue().launch(debug=False, share=False,
                        server_name='127.0.0.1', server_port=8080)
