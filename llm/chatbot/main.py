import logging
import os
import sys
from typing import Any

import gradio as gr

import pymongo

from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader, Document
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent import ReActAgent
from llama_index.core.settings import Settings
from llama_index.core.base.agent.types import StreamingAgentChatResponse


# --- Configuration & Initialization ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Initialize Gemini LLM & Embeddings
Settings.llm = Gemini(api_key=os.getenv("GEMINI_API_KEY"),
                      model_name="models/gemini-1.5-flash-latest") # Changed to a standard model name
Settings.embed_model = GeminiEmbedding(api_key=os.getenv(
    "GEMINI_API_KEY"), model_name="models/text-embedding-004")

# Initialize MongoDB Atlas
# --- Configuration ---
MONGO_PASSWORD = os.getenv("MONGODB_PASSWORD")
if not MONGO_PASSWORD:
    logging.error(
        "Error: MONGODB_PASSWORD environment variable not set.")
    sys.exit(1)

MONGO_DB = "MYMONGODB"
MONGO_HOST = "host.mongodb.net"
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
    async def _acall(self, *args: Any, **kwargs: Any) -> str:
        # ReActAgent passes query in 'input' kwarg
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
                    f"RAG query for '{query_str}' yielded no text response. Source nodes found: {num_source_nodes}")
                if num_source_nodes == 0:
                    return "No relevant documents were found in the knowledge base to answer the query."
                else:
                    return "Relevant documents were found, but no direct answer could be synthesized from them."
            return actual_response_str
        except Exception as e:
            logging.error(
                f"Error during RobustQueryEngineTool._acall for query '{query_str}': {e}", exc_info=True)
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
                "best practices, and other contextual details from uploaded documents in the knowledge base. "
                "For example, ask 'What is the formula for X?' or 'Explain Y best practices.'"
            )
        )
        tools_for_agent = [knowledge_base_tool]
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
async def finance_chat_bot_logic(message: str | None,
                                 history_list_of_lists: list,  # [[user, bot], [user, bot], ...]
                                 session_state: dict,
                                 current_actions_log_content: str):
    global agent

    # Ensure current_actions_log_content is initialized if None (should not happen with value set)
    if current_actions_log_content is None:
        current_actions_log_content = initialization_logs
    elif not isinstance(current_actions_log_content, str): # Ensure it's a string
        current_actions_log_content = str(current_actions_log_content)

    turn_specific_log_entries = []

    if not agent:
        error_msg = "ERROR: Agent not initialized. Chat interface cannot function."
        turn_specific_log_entries.append(error_msg)
        logging.error(error_msg)
        if message: # Only yield error if there was a user message trying to be processed
            yield "Agent is not ready. Please check the application logs."
        new_full_log = current_actions_log_content + "\n\n" + "\n".join(turn_specific_log_entries) # Added extra newline for spacing
        yield "", session_state, new_full_log # Yield empty chat string, state, and log
        return

    # Handle "Clear" button click (message is None from gr.ChatInterface clear_btn)
    if message is None:
        agent.reset()
        turn_specific_log_entries.append("SYSTEM: New conversation started by button. Memory has been cleared.")
        logging.info("New conversation started via clear button (message is None).")
        session_state["chat_history"] = [] # Reset our state's history tracker
        # No chat message to yield. gr.ChatInterface handles clearing the chat display.
        new_full_log = current_actions_log_content + "\n\n" + "\n".join(turn_specific_log_entries)
        yield "", session_state, new_full_log # Yield empty chat string, state, and log for additional_outputs
        return

    # Handle user message
    turn_specific_log_entries.append(f"User: {message}")
    turn_specific_log_entries.append("Chatbot thinking...")

    # Handle "new conversation" text command (optional, clear_btn is primary)
    if message.lower().strip() == "new conversation":
        agent.reset()
        bot_response = "Okay, I've started a new conversation. How can I help you?"
        turn_specific_log_entries.append("SYSTEM: New conversation started by text command. Memory has been cleared.")
        logging.info(
            "New conversation started by user input 'new conversation'.")
        session_state["chat_history"] = [] # Reset our state's history tracker
        yield bot_response # Stream bot response
        new_full_log = current_actions_log_content + "\n\n" + "\n".join(turn_specific_log_entries)
        yield bot_response, session_state, new_full_log # Yield final chat, state, and log
        return

    try:
        response_payload = await agent.astream_chat(message)
        full_response_text = ""
        final_stream_sources = []

        if not isinstance(response_payload, StreamingAgentChatResponse):
            error_detail = f"Unexpected response type from agent: {type(response_payload)}. Expected StreamingAgentChatResponse."
            turn_specific_log_entries.append(f"ERROR: {error_detail}")
            logging.error(error_detail)
            full_response_text = "Error: Could not process agent response due to unexpected type."
            yield full_response_text # Stream error to chat
            new_full_log = current_actions_log_content + "\n\n" + "\n".join(turn_specific_log_entries)
            yield full_response_text, session_state, new_full_log # Yield final chat, state, and log
            return

        logging.info(
            "Received StreamingAgentChatResponse object. Processing stream...")
        turn_specific_log_entries.append("INFO: Processing agent response stream...")

        async for text_token in response_payload.async_response_gen():
            if text_token:
                full_response_text += text_token
                yield full_response_text # Stream to gr.ChatInterface

        if not full_response_text:
            response_obj = getattr(response_payload, 'response', None)
            if response_obj:
                actual_response_str = getattr(response_obj, 'response', None)
                if actual_response_str:
                    logging.info(
                        "Stream yielded no text, using fallback from response_payload.response.response.")
                    full_response_text = actual_response_str
                    yield full_response_text # Yield the fallback

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
            turn_specific_log_entries.append("No explicit tool sources reported by the agent for this interaction.")

        session_state["chat_history"] = history_list_of_lists # Update our state tracker
        new_full_log = current_actions_log_content + "\n\n" + "\n".join(turn_specific_log_entries) # Added extra newline
        yield full_response_text, session_state, new_full_log # Yield final chat, state, and log
        return

    except Exception as e:
        error_msg = f"Sorry, an error occurred: {str(e)}"
        logging.error(f"Error during chat stream: {e}", exc_info=True)
        turn_specific_log_entries.append(f"ERROR processing your request: {e}")
        yield error_msg # Stream error to chat
        new_full_log = current_actions_log_content + "\n\n" + "\n".join(turn_specific_log_entries)
        yield error_msg, session_state, new_full_log # Yield final chat, state, and log
        return

# --- Gradio Interface Definition ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", secondary_hue="orange"), title="Finance Chatbot Expert") as demo:
    gr.Markdown(
        """
        # 💰 Finance Chatbot Expert 🤖 (using gr.ChatInterface)
        Ask me about stock prices, company overviews, financial formulas (from my knowledge base), or ask me to detect anomalies in numerical data!
        Click "🔄 Start New Conversation" to clear memory and start fresh.
        Watch out for the "Actions Log" to see what I'm doing behind the scenes!
        """
    )
    # session_state for agent's memory and other potential state variables
    session_data_state = gr.State(value={"chat_history": []})

    with gr.Row():
        with gr.Column(scale=3):  # Make chat area wider
            # actions_taken_display must be defined before ChatInterface if used in additional_inputs/outputs
            # However, it's better to define it in its layout column and then reference it.
            # Gradio allows components to be referenced across the layout for inputs/outputs.
            # Placeholder for actions_taken_display, will be defined in the other column
            actions_taken_display_ref = gr.Textbox(visible=False) # Dummy for type hinting if needed early

            chat_ui = gr.ChatInterface(
                fn=finance_chat_bot_logic,
                # additional_inputs will be passed to fn after message and history
                # Values from these components are passed.
                additional_inputs=[session_data_state, actions_taken_display_ref],
                # additional_outputs will be updated by the return values of fn (after all yields)
                # The components themselves are passed here.
                # Order of return values from fn: (new_session_state_value, new_actions_log_value)
                # must match order of components in additional_outputs list.
                chatbot=gr.Chatbot(
                    label="Conversation",
                    bubble_full_width=False,
                    avatar_images=(None, "https://img.icons8.com/fluency/96/chatbot.png"),
                    height=700,
                ),
                textbox=gr.Textbox(
                    label="Your Message:",
                    placeholder="e.g., 'What's the price of AAPL?', 'Detect anomalies in: {\"data\": [10,12,150,13]}', 'What is P/E ratio?'",
                    lines=1,
                    show_label=False # Cleaner look with placeholder as primary cue
                ),
            )
        with gr.Column(scale=2):  # Make action log area wider
            gr.Markdown("## 📝 Actions Log")
            actions_taken_display = gr.Textbox(
                label="Chatbot Actions & System Logs",
                lines=35,
                interactive=False,
                max_lines=40, # Increased max_lines
                value=initialization_logs  # Display initial logs
            )

    # Connect the actual actions_taken_display to the ChatInterface
    # This is done by ensuring the references in additional_inputs/outputs point to the correct component.
    # We defined actions_taken_display_ref as a placeholder. Now we ensure chat_ui uses the real one.
    # This is a bit of a Gradio trick: gr.ChatInterface needs the component *instances*.
    # By defining actions_taken_display in the layout, it's created.
    # Then we pass this instance to additional_inputs and additional_outputs of chat_ui.
    chat_ui.additional_inputs = [session_data_state, actions_taken_display]
    chat_ui.additional_outputs = [session_data_state, actions_taken_display]


if __name__ == "__main__":
    logging.info("Starting Gradio app with streaming support...")
    print("Initialization logs (also in UI on startup):\n", initialization_logs)
    print("Finance Chatbot Expert is starting. Access it at the URL provided by Gradio.")
    # .queue() is important for handling multiple users/requests and streaming
    demo.queue().launch(debug=False, share=False)
