import asyncio
import logging
import os
import re
import sys
import time
from typing import Any, AsyncGenerator, Dict, List, Tuple
import urllib3

from llama_index.core import Settings
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.llama_pack.base import BaseLlamaPack
from llama_index.core.llms import ChatMessage
from llama_index.core.memory import Memory
from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context, WorkflowRuntimeError
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import (
    AgentInput,
    AgentOutput,
    AgentSetup,
    AgentStream,
    ToolCall,
    ToolCallResult,
)

import gradio as gr

from libs.prompts import SystemPrompt
from styles.common import CustomCSS, FooterCSS, AuthHTML
from tools.math.base import MathTool
from tools.docs.base import DocumentTool


def setup_logging():
    """Configure logging for the application."""
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

    console_handler = logging.StreamHandler(sys.__stdout__)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Suppress verbose logs from specific libraries
    for lib in os.getenv("LOG_LIBS", "pymongo,urllib3,httpcore,matplotlib,httpx").split(","):
        logging.getLogger(lib).setLevel(logging.ERROR)

    return logging.getLogger(__name__)


logger = setup_logging()

# LLM Configuration
MODEL = "qwen/qwen3-8b"
EMBED_MODEL = "text-embedding-nomic-embed-text-v1.5"
LMSTUDIO_HOST = os.getenv("LMSTUDIO_HOST", "http://127.0.0.1:1234/v1")

try:
    timeout = urllib3.Timeout(connect=2.0, read=7.0)
    http = urllib3.PoolManager(timeout=timeout)
    response = http.request("GET", f"{LMSTUDIO_HOST}")
    if response.status == 200:
        logger.info("Connected to LMStudio API successfully.")
    else:
        logger.error(
            f"Failed to connect to LMStudio API: {response.status}")
except urllib3.exceptions.HTTPError as e:
    logger.error(f"Error connecting to LMStudio API: {e}")
    sys.exit(1)

Settings.llm = OpenAI(
    model_name=MODEL,
    api_base=LMSTUDIO_HOST,
    thinking=False,
    temperature=0.0,
    max_retries=5,
    context_window=8096,
)

Settings.embed_model = OpenAIEmbedding(
    model_name=EMBED_MODEL,
    api_base=LMSTUDIO_HOST,
)

# Tools Configuration
document_tool = DocumentTool()
SUPPORTED_TOOLS = MathTool().to_tool_list() + document_tool.to_tool_list()


class GradioReActAgentPack(BaseLlamaPack):

    def __init__(self, supported_tools: List[FunctionTool]) -> None:
        self.memory = Memory.from_defaults(token_limit=32768)
        self.conversation_history: List[ChatMessage] = []
        self.document_tool = document_tool

        self.agent = FunctionAgent(
            tools=list(supported_tools),
            verbose=False,
            memory=self.memory,
            max_iterations=3,
            system_prompt=SystemPrompt(),
        )

        self.context: Context = Context(workflow=self.agent)

    def _load_document_from_file(self, file_path: str) -> bool:
        """Load single document into document tool for vector search."""
        try:
            logger.info(f"Loading document: {file_path}")

            # Update the document tool with the document
            self.document_tool.update_document(file_path)

            # Ensure indexes are built
            time.sleep(0.1)

            logger.info(f"Loaded document into vector index: {file_path}")
            return True

        except (OSError, IOError, ValueError) as e:
            logger.error(f"Error loading document: {e}")
            return False

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {
            "agent": self.agent,
            "llm": Settings.llm,
            "tools": SUPPORTED_TOOLS,
            "context": self.context,
            "memory": self.memory,
        }

    def _handle_user_message(self, user_message, history):
        """Handle user submitted message and update history."""
        if isinstance(user_message, dict):
            # Handle files if present
            files = user_message.get("files", [])
            if files:
                logger.info(f"Processing {len(files)} uploaded files")

                # Load the first (and likely only) document
                first_file = files[0] if files else None
                success = self._load_document_from_file(
                    first_file) if first_file else False

                # Add file information to history
                if success:
                    file_info = "📁 Uploaded document file - ready for search and analysis"
                    logger.info(
                        f"Document loaded successfully. Vector index: "
                        f"{self.document_tool.vector_index is not None}")
                else:
                    file_info = "⚠️ No document file found or error loading document"

                history.append({"role": "user", "content": file_info})
                logger.info(f"Document processing result: {success}")

            user_text = user_message.get("text", "")
            if user_text:
                history.append({"role": "user", "content": user_text})
                logger.info(f"User text message: {user_text}")
        else:
            # Handle simple string message
            user_text = user_message
            if user_text:
                history.append({"role": "user", "content": user_text})
                logger.info(f"User message: {user_text}")

        return "", history

    def _get_status_message(self, event, current_user_msg: str,
                            thinking_count: int) -> tuple[str | None, int]:
        """Get status message for different event types."""
        if isinstance(event, ToolCall):
            return f"🧰 **Calling tool** `{event.tool_name}`", 0
        elif isinstance(event, AgentSetup):
            return "⚙️ **Setting up agent...**", 0
        elif isinstance(event, AgentInput):
            return f"⏳ **Processing...** {current_user_msg}", 0
        elif isinstance(event, ToolCallResult):
            return f"✅ **Tool `{event.tool_name}` Executed**", 0
        elif isinstance(event, AgentOutput):
            return "🎉 **Response generated**", 0
        elif isinstance(event, AgentStream):
            thinking_count += 1
            if thinking_count % 10 == 1:
                dots = "." * (1 + (thinking_count // 10) % 3)
                return f"🤔 **Thinking{dots}**", thinking_count

        return None, thinking_count

    async def _stream_agent_events(
        self, handler, chat_history: List[Dict[str, str]], current_user_msg: str
    ) -> AsyncGenerator[List[Dict[str, str]], None]:
        """Stream agent events and provide real-time status updates."""
        response_content = ""
        last_status = None
        thinking_count = 0

        async for event in handler.stream_events():
            logger.debug(f"Received event: {type(event).__name__} - {event}")

            status_message, thinking_count = self._get_status_message(
                event, current_user_msg, thinking_count)

            if isinstance(event, AgentOutput):
                # Clean the content as it comes in
                new_content = event.response.content or ""
                logger.debug(f"Raw AgentOutput content: {new_content[:200]}...")
                cleaned_new_content = self._clean_response_content(new_content)
                logger.debug(f"Cleaned AgentOutput content: {cleaned_new_content[:200]}...")
                response_content = cleaned_new_content

            if status_message and status_message != last_status:
                status_history = chat_history[:-1] + [
                    {"role": "user", "content": chat_history[-1]["content"]},
                    {"role": "assistant", "content": status_message}
                ]
                yield status_history
                last_status = status_message

                sleep_time = 0.3 if status_message.startswith(
                    "🤔 **Thinking") else 0.7
                await asyncio.sleep(sleep_time)

            if response_content:
                streaming_history = chat_history[:-1] + [
                    {"role": "user", "content": chat_history[-1]["content"]},
                    {"role": "assistant", "content": response_content}
                ]
                yield streaming_history

    def _rebuild_memory(self):
        """Rebuild memory from conversation history."""
        self.memory.reset()
        for msg in self.conversation_history:
            self.memory.put(msg)

    def _clean_response_content(self, response_content: str | None) -> str:
        """Clean response content from unwanted prefixes and thinking tags."""
        if not response_content:
            return ""

        content = response_content

        # Remove <think>...</think> tags completely (for LMStudio)
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)

        # Remove assistant:/user: prefixes (for Ollama compatibility)
        content = re.sub(
            r"^[\s\n\r]*(assistant:|user:)[\s\n\r]*",
            "",
            content,
            flags=re.IGNORECASE
        )

        # Clean up extra whitespace and newlines
        return content.strip()

    def _create_history_update(self, chat_history: List[Dict[str, str]],
                               response_content: str) -> List[Dict[str, str]]:
        """Create updated chat history."""
        return chat_history[:-1] + [
            {"role": "user", "content": chat_history[-1]["content"]},
            {"role": "assistant", "content": response_content}
        ]

    async def _generate_response(
        self, chat_history: List[Dict[str, str]]
    ) -> AsyncGenerator[List[Dict[str, str]], None]:
        """Generate response from agent."""
        self._rebuild_memory()

        current_user_msg = chat_history[-1]["content"]
        current_user_message = ChatMessage(
            role="user", content=current_user_msg)

        logger.info(f"Document tool state before agent run: "
                    f"document={self.document_tool.document is not None}, "
                    f"vector_index={self.document_tool.vector_index is not None}, "
                    f"summary_index={self.document_tool.summary_index is not None}")
        logger.info(
            f"Chat history length: {len(chat_history)}, last message: '{current_user_msg}'")

        try:
            handler = self.agent.run(
                user_msg=current_user_msg,
                memory=self.memory,
                ctx=self.context
            )

            async for update in self._stream_agent_events(handler, chat_history,
                                                          current_user_msg):
                yield update

            try:
                agent_response = await handler
                response_content = agent_response.response.content if isinstance(
                    agent_response.response, ChatMessage) else str(agent_response.response)
                response_content = self._clean_response_content(
                    response_content)
            except (AttributeError, TypeError, asyncio.TimeoutError,
                    WorkflowRuntimeError) as e:
                logger.error(f"Error during agent execution: {e}")
                response_content = f"❌ **Error**: {str(e)}"

        except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
            logger.error(f"Error during agent execution: {e}")
            response_content = f"❌ **Error**: {str(e)}"

        # Update conversation history with ChatMessage objects
        if not any(msg.content == current_user_message.content and
                   msg.role == "user" for msg in self.conversation_history):
            self.conversation_history.append(current_user_message)
            self.memory.put(current_user_message)

        assistant_message = ChatMessage(
            role="assistant", content=response_content)
        self.conversation_history.append(assistant_message)
        self.memory.put(assistant_message)

        yield self._create_history_update(chat_history, response_content)

    async def _reset_chat(self) -> Tuple[str, List]:
        """Reset the agent's chat history and clear all dialogue boxes."""
        self.memory.reset()
        self.conversation_history.clear()

        # Clear document tool document
        self.document_tool.update_document("")

        # Reset the context state by creating a new instance of the state class.
        state = await self.context.store.get_state()
        await self.context.store.set_state(state.__class__())
        return "", []

    def _create_header(self):
        """Create the header section of the UI."""
        with gr.Row(equal_height=True):
            with gr.Column(scale=2):
                gr.Markdown("""
                    <div class="logo-container">
                        <div class="logo-circle">
                            <div class="logo-shine"></div>
                            <span class="logo-icon">✨</span>
                        </div>
                    </div>
                    """)
            with gr.Column(scale=8):
                gr.Markdown("""
                    <div class="header-welcome">
                        <h1 class="header-title">Smart Assistant</h1>
                        <p class="header-subtitle">Your intelligent conversation partner</p>
                    </div>
                    """)

    def _create_controls(self):
        """Create control buttons."""
        with gr.Row():
            with gr.Column(scale=5):
                clear = gr.ClearButton(
                    value="New Chat",
                    elem_id="clear_button",
                    size="sm",
                    icon="https://img.icons8.com/fluency/48/full-trash.png",
                    variant="primary",
                )
            with gr.Column(scale=5):
                gr.Button(
                    value="Logout",
                    elem_id="logout_button",
                    link="/logout",
                    size="sm",
                    icon="https://img.icons8.com/fluency/48/logout-rounded-left.png",
                    variant="secondary",
                )
        return clear

    def _handle_like(self, data: gr.LikeData):
        if data.liked:
            print("You upvoted this response: ", data.value)
        else:
            print("You downvoted this response: ", data.value)

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run chat with ReActAgent."""
        with gr.Blocks(theme="default", css=CustomCSS(), title="Smart Assistant") as chatbot:
            self._create_header()

            with gr.Row():
                chat_window = gr.Chatbot(
                    elem_id="chatbot",
                    type="messages",
                    avatar_images=(
                        "https://img.icons8.com/fluency/48/emily-bronte.png",
                        "https://img.icons8.com/fluency/48/electronic-brain.png"
                    ),
                    render_markdown=True,
                    autoscroll=True,
                    height=640,
                    show_label=False,
                    bubble_full_width=False
                )
                # https://www.gradio.app/4.44.1/docs/gradio/chatinterface
                chat_window.like(self._handle_like, None, None)

            with gr.Row():
                chat_input = gr.MultimodalTextbox(
                    elem_id="chat_input",
                    interactive=True,
                    placeholder="Type your message here... (Press ENTER ↲ to send)",
                    show_label=False,
                    container=False
                )

            clear = self._create_controls()

            with gr.Row():
                gr.HTML(FooterCSS())

            # Event handlers
            chat_input.submit(
                self._handle_user_message,
                [chat_input, chat_window],
                [chat_input, chat_window],
                queue=True,
            ).then(
                self._generate_response,
                chat_window,
                [chat_window],
            )
            clear.click(self._reset_chat, None, [
                        chat_input, chat_window], api_name=None)

        chatbot.launch(
            server_name="0.0.0.0",
            server_port=8000,
            favicon_path="assets/logo.png",
            auth=None,
            auth_message=AuthHTML(),
            allowed_paths=["assets/logo.png"],
        )


if __name__ == "__main__":
    GradioReActAgentPack(supported_tools=SUPPORTED_TOOLS).run()
