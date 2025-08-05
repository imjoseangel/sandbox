import asyncio
import logging
import os
import re
import sys
from typing import Any, AsyncGenerator, Dict, List, Tuple

from llama_index.core import PromptTemplate
from llama_index.core import Settings
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.llama_pack.base import BaseLlamaPack
from llama_index.core.llms import ChatMessage
from llama_index.core.memory import Memory
from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context
from llama_index.llms.ollama import Ollama
from llama_index.core.agent.workflow import (
    AgentInput,
    AgentOutput,
    AgentSetup,
    AgentStream,
    ToolCall,
    ToolCallResult,
)

import gradio as gr

from libs.prompts import SystemPrompt, ReactPrompt
from styles.common import CustomCSS, FooterCSS, AuthHTML
from tools.math.base import MathTool


# --- Start Logging Configuration ---
logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

root_logger = logging.getLogger()
root_logger.setLevel(os.getenv("LOG_LEVEL", "DEBUG"))

console_handler = logging.StreamHandler(sys.__stdout__)
console_handler.setFormatter(formatter)
root_logger.addHandler(console_handler)

libs = os.getenv(
    "LOG_LIBS", "pymongo,urllib3,httpcore,matplotlib,httpx").split(",")

for lib in libs:
    logging.getLogger(lib).setLevel(logging.ERROR)


# --- End Logging Configuration ---

# --- Start LLM Configuration ---

MODEL = "qwen3:30b"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

Settings.llm = Ollama(
    model=MODEL,
    base_url=OLLAMA_HOST,
    temperature=0,
    max_retries=5,
    context_window=3024,
    system_prompt=SystemPrompt(),
)

# --- End LLM Configuration ---

# --- Start Tools Enablement ---

tool_spec = MathTool()

SUPPORTED_TOOLS = tool_spec.to_tool_list()

# --- End Tools Enablement ---


class GradioReActAgentPack(BaseLlamaPack):

    def __init__(self, supported_tools: List[FunctionTool],
                 **kwargs: Any,) -> None:
        self.memory = Memory.from_defaults(token_limit=32768)
        self.conversation_history: List[ChatMessage] = []
        self.react_prompt = PromptTemplate(ReactPrompt())

        self.agent = ReActAgent(
            tools=list(supported_tools),
            verbose=True,
            memory=self.memory,
            max_iterations=10,
        )
        self.agent.update_prompts({
            "react_header": self.react_prompt,
            "react_chat_refine": PromptTemplate(
                "You MUST use tools to refine this answer. Current response: {existing_answer}\n"
                "Now use appropriate tools to improve it."
            )
        })
        self.context: Context = Context(workflow=self.agent)

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
        """
        Handle the user submitted message. Clear message box, and append
        to the history.
        """
        if isinstance(user_message, dict):
            user_text = user_message.get("text", "")
        else:
            user_text = user_message

        logger.info(f"User message received: {user_text}")

        # Convert to messages format instead of tuples
        new_message = {"role": "user", "content": user_text}
        return "", [*history, new_message]

    async def _stream_agent_events(
        self,
        handler,
        chat_history: List[Dict[str, str]],
        current_user_msg: str
    ) -> AsyncGenerator[List[Dict[str, str]], None]:
        """
        Stream agent events and provide real-time status updates.
        """

        response_content = ""
        last_status = None

        async for event in handler.stream_events():
            status_message = None

            logger.debug(f"Received event: {type(event).__name__} - {event}")

            if isinstance(event, ToolCall):
                tool_name = event.tool_name
                _ = ", ".join(
                    f"{k}='{v}'" for k, v in event.tool_kwargs.items())
                status_message = f"🧰 **Calling tool**: `{tool_name}`"
            elif isinstance(event, AgentSetup):
                status_message = f"⚙️ **Setting up agent...** {event.setup_info}"
            elif isinstance(event, AgentInput):
                status_message = f"⌨️ **Processing...**: {current_user_msg}"
            elif isinstance(event, AgentStream):
                status_message = "🤔 **Thinking...**"
            elif isinstance(event, ToolCallResult):
                status_message = f"✅ **Tool `{event.tool_name}` Executed**"
            elif isinstance(event, AgentOutput):
                response_content += event.response.content or ""
                status_message = "🎉 **Response generated**"

            if status_message and status_message != last_status:
                status_history = chat_history[:-1] + \
                    [{"role": "user", "content": chat_history[-1]["content"]},
                        {"role": "assistant", "content": status_message}]
                yield status_history
                last_status = status_message
                await asyncio.sleep(0.3)

            if response_content:
                # Stream final response as it comes in
                streaming_history = chat_history[:-1] + \
                    [{"role": "user", "content": chat_history[-1]["content"]},
                        {"role": "assistant", "content": response_content}]
                yield streaming_history

    async def _generate_response(
        self, chat_history: List[Dict[str, str]]
    ) -> AsyncGenerator[List[Dict[str, str]], None]:
        """
        Generate the response from agent, and capture the stdout of the
        ReActAgent's thoughts.
        """
        # Clear memory and rebuild from our stored conversation history
        self.memory.reset()

        # Rebuild entire conversation from stored history first
        for msg in self.conversation_history:
            self.memory.put(msg)

        # Get the current user message
        current_user_msg = chat_history[-1]["content"]
        current_user_message = ChatMessage(
            role="user", content=current_user_msg)

        try:
            handler = self.agent.run(user_msg=current_user_msg,
                                     memory=self.memory,
                                     ctx=self.context)

            async for update in self._stream_agent_events(handler, chat_history,
                                                          current_user_msg):
                yield update

            # Await the final response object to ensure completion
            response = await handler

            if isinstance(response.response, ChatMessage):
                response_content = response.response.content or ""
            else:
                response_content = str(response.response)

            response_content = re.sub(
                r"^[\s\n\r]*(assistant:|user:)[\s\n\r]*",
                "",
                response_content or "",
                flags=re.IGNORECASE
            )

        except Exception as e:
            logger.error(f"Error during agent execution: {e}")
            response_content = f"❌ **Error**: {str(e)}"

        # Store the conversation in our persistent history (only if not already there)
        if not any(msg.content == current_user_message.content and
                   msg.role == "user" for msg in self.conversation_history):
            self.conversation_history.append(current_user_message)

        assistant_message = ChatMessage(
            role="assistant", content=response_content)
        self.conversation_history.append(assistant_message)
        self.memory.put(assistant_message)

        updated_history = chat_history[:-1] + \
            [{"role": "user", "content": chat_history[-1]["content"]},
             {"role": "assistant", "content": response_content}]
        yield updated_history

    async def _reset_chat(self) -> Tuple[str, List]:
        """Reset the agent's chat history. And clear all dialogue boxes."""
        self.memory.reset()
        self.conversation_history.clear()
        # Reset the context state by creating a new instance of the state class.
        state = await self.context.store.get_state()
        await self.context.store.set_state(state.__class__())
        return "", []

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run chat with ReActAgent."""

        # Define custom CSS for borders on both chat components
        custom_css = CustomCSS()

        with gr.Blocks(theme="default", css=custom_css,
                       title="Smart Assistant") as chatbot:
            with gr.Row(equal_height=True):
                with gr.Column(scale=2):
                    gr.Markdown("""
                        <div style="display: flex; align-items: center; justify-content: center; width: 100%; background: #f3f4f6; padding: 35px; border-radius: 12px; border-left: 4px;">
                            <img src="/gradio_api/file=assets/logo.png" style="width: auto; height: 50px; margin-top: 10px; margin-bottom: 10px;" />
                        </div>
                        """)
                with gr.Column(scale=8):
                    gr.Markdown(
                        """
                        <div style="background: linear-gradient(90deg, #f0f9ff 0%, #e0f2fe 100%);
                        padding: 20px; border-radius: 12px; border-left: 4px solid #0369a1;">
                        <h1 style="color: #0369a1;">🤖 Smart Assistant</h1>
                        <p>Welcome to your smart assistant! Get instant insights with natural language.</p>
                        </div>
                        """
                    )
            with gr.Row():
                chat_window = gr.Chatbot(
                    elem_id="chatbot",
                    type="messages",
                    avatar_images=(
                        "https://img.icons8.com/fluency/48/emily-bronte.png",
                        "https://img.icons8.com/fluency/48/electronic-brain.png"),
                    render_markdown=True,
                    autoscroll=True,
                    height=640,
                    show_label=False
                )
            with gr.Row():
                chat_input = gr.MultimodalTextbox(
                    elem_id="chat_input",
                    interactive=True,
                    placeholder="Enter message...",
                    show_label=False
                )
            with gr.Row():
                with gr.Column(scale=5):
                    clear = gr.ClearButton(
                        elem_id="clear_button",
                        size="sm",
                        icon="https://img.icons8.com/fluency/48/full-trash.png",
                    )
                with gr.Column(scale=5):
                    gr.Button(
                        "Logout",
                        elem_id="logout_button",
                        link="/logout",
                        size="sm",
                        icon="https://img.icons8.com/fluency/48/logout-rounded-left.png",
                    )
            with gr.Row():
                gr.HTML(FooterCSS())
            chat_input.submit(
                self._handle_user_message,
                [chat_input, chat_window],
                [chat_input, chat_window],
                queue=False,
            ).then(
                self._generate_response,
                chat_window,
                [chat_window],
            )
            clear.click(self._reset_chat, None, [
                        chat_input, chat_window], api_name=None)

        chatbot.launch(server_name="0.0.0.0", server_port=8000,
                       favicon_path="assets/logo.png", auth=None,
                       auth_message=AuthHTML(),
                       allowed_paths=["assets/logo.png"],)


if __name__ == "__main__":
    GradioReActAgentPack(supported_tools=SUPPORTED_TOOLS,
                         run_from_main=True).run()
