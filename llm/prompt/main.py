import logging
import threading
import re
import sys

from llama_index.core import PromptTemplate
from llama_index.core import Settings
from llama_index.core.agent import ReActAgent
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.llms.gemini import Gemini

import gradio as gr

# --- Configuration ---

logger = logging.getLogger(__name__)
# Define your log format
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Get the root logger and configure it
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)


# Configure Console Handler to output to actual console
console_handler = logging.StreamHandler(sys.__stdout__)
console_handler.setFormatter(formatter)

root_logger.addHandler(console_handler)


MODEL = "models/gemini-1.5-flash-latest"

Settings.llm = Gemini(
    model=MODEL,
    request_timeout=120.0,
    temperature=0.0,
    context_window=2048,
)

react_system_header_str = """\
You are an advanced assistant that MUST use tools for EVERY user query without exception. Follow these rules ABSOLUTELY:

## ABSOLUTE RULES
1. **MANDATORY FIRST TOOL USE**: For EVERY user query, your FIRST response MUST be a tool call (Action). No exceptions.
2. **NO MEMORY DEPENDENCE**: Never rely on conversation history or previous answers - always use tools to get fresh information.
3. **STRICT SEQUENCE**: Follow this exact sequence for every query:
   - Thought: Analyze the query
   - Action: Call a tool (required first step)
   - Observation: Tool result
   - [Repeat Thought/Action/Observation if needed]
   - Answer: Final response using ONLY current turn's tool outputs

## TOOL USAGE PROTOCOL
1. **ALWAYS START WITH TOOL**: Even if you think you know the answer, you MUST begin with a tool call.
2. **REFRESH DATA**: For repeated queries, use tools again to get fresh data - never reuse old observations.
3. **TOOL SELECTION**: Choose the most specific tool available for each query.

## TOOLS AVAILABLE
{tool_desc}

## OUTPUT FORMAT
Follow this exact format for EVERY response:

Thought: [Analyze the query and select tool]
Action: [tool_name]
Action Input: {{"input": "query"}}
Observation: [tool result]
Answer: [Final response using ONLY current observations]

## EXAMPLES
**User:** What contracts are available?
**Thought:** User asks for available contracts. Must use available_contracts_listing tool.
**Action:** available_contracts_listing
**Action Input:** {{}}
**Observation:** ["Contract A", "Contract B"]
**Answer:** The available contracts are:
- Contract A
- Contract B

**User:** Tell me about Contract A
**Thought:** Need details about Contract A. Must use knowledge_base_retriever.
**Action:** knowledge_base_retriever
**Action Input:** {{"input": "details about Contract A"}}
**Observation:** [Contract details...]
**Answer:** Contract A details: [...]
"""

react_system_prompt = PromptTemplate(react_system_header_str)
chat_memory = ChatMemoryBuffer.from_defaults(token_limit=8196)

agent = ReActAgent.from_tools(
    tools=[
    ],
    llm=Settings.llm,
    memory=chat_memory,
    verbose=True,
    max_iterations=10,
    tool_retriever=None,
    context="You MUST use tools for EVERY query without exception",
    callback_manager=Settings.callback_manager,
)

agent.update_prompts({
    "react_header": react_system_prompt,
    "react_chat_refine": PromptTemplate(
        "You MUST use tools to refine this answer. Current response: {existing_answer}\n"
        "Now use appropriate tools to improve it."
    )
})


class StdOutToLogger:
    """
    A class to redirect stdout to a Python logger, stripping ANSI codes.
    """

    def __init__(self, logger_instance, log_level=logging.INFO):
        self.logger = logger_instance
        self.log_level = log_level
        self.line_buffer = ""
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        self._thread_local_capture = threading.local()

    def start_capture(self):
        """Starts capturing stdout lines for the current thread."""
        self._thread_local_capture.lines = []

    def stop_capture(self) -> list[str]:
        """Stops capturing stdout lines for the current thread and returns them."""
        captured = getattr(self._thread_local_capture, 'lines', None)
        if hasattr(self._thread_local_capture, 'lines'):
            del self._thread_local_capture.lines
        return captured if captured is not None else []

    def is_capturing(self) -> bool:
        """Returns True if capturing is active for the current thread."""
        return hasattr(self._thread_local_capture, 'lines')

    def write(self, message: str):
        self.line_buffer += message
        while '\n' in self.line_buffer:
            line, self.line_buffer = self.line_buffer.split('\n', 1)
            stripped_line = self.ansi_escape.sub('', line)
            if stripped_line.strip():
                self.logger.log(self.log_level, stripped_line)
                if hasattr(self._thread_local_capture, 'lines'):
                    self._thread_local_capture.lines.append(stripped_line)

    def flush(self):
        if self.line_buffer.strip():
            line_to_log = self.ansi_escape.sub('', self.line_buffer)
            if line_to_log.strip():
                self.logger.log(self.log_level, line_to_log)
                if hasattr(self._thread_local_capture, 'lines'):
                    self._thread_local_capture.lines.append(line_to_log)
            self.line_buffer = ""

    def isatty(self):
        # Make it appear as a TTY to encourage full output from libraries
        return True


stdout_redirector = StdOutToLogger(logger, log_level=logging.DEBUG)
sys.stdout = stdout_redirector
logger.info(
    "Successfully redirected sys.stdout to the logging system.")


def chat_bot_logic(message: str, gradio_history: list, session_state: dict):
    if not message or not message.strip():
        return "Please enter a non-empty message."

    if not gradio_history:
        session_state["chat_history"] = []
        logger.info("Reset chat history for new session")

    agent.reset()

    stdout_capturer = stdout_redirector
    stdout_capturer.start_capture()

    try:
        tool_enforced_prompt = (
            f"REMEMBER: You MUST use tools for this query. User asked: {message}\n"
            "Select the most appropriate tool now."
        )

        response_obj = agent.chat(
            tool_enforced_prompt,
            chat_history=session_state.get("chat_history", [])
        )

        captured_lines_attempt1 = stdout_capturer.stop_capture()
        action_logged_attempt1 = any(
            "Action:" in line for line in captured_lines_attempt1)

        if not action_logged_attempt1:
            logger.warning(
                f"Agent did not log an 'Action:' for query '{message}'. "
                "Forcing tool use with re-prompt."
            )
            stdout_capturer.start_capture()
            response_obj = agent.chat(
                f"CRITICAL: You MUST use a tool and log 'Action:'. Original query: {message}",
                chat_history=session_state.get("chat_history", [])
            )
            captured_lines_attempt2 = stdout_capturer.stop_capture()

            if not any("Action:" in line for line in captured_lines_attempt2):
                logger.error(
                    f"Agent STILL did not log an 'Action:' on re-prompt for query '{message}'. "
                    f"Response: {str(response_obj)}"
                )
            else:
                logger.info(
                    f"Agent logged 'Action:' on re-prompt for query '{message}'.")

        final_response_str = str(response_obj)

        updated_history = session_state.get("chat_history", [])
        updated_history.extend([
            ChatMessage(role=MessageRole.USER, content=message),
            ChatMessage(role=MessageRole.ASSISTANT, content=final_response_str)
        ])
        session_state["chat_history"] = updated_history

        return final_response_str

    except Exception as e:
        logger.error(f"Error in chat_bot_logic: {str(e)}", exc_info=True)
        if getattr(stdout_capturer, "is_capturing", lambda: False)():
            stdout_capturer.stop_capture()
        return f"Error processing request: {str(e)}"


with gr.Blocks(theme=gr.themes.Citrus(primary_hue="blue"), title="Chatbot") as demo:
    gr.HTML("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600&display=swap');
        body { background: #f8fafc; font-family: 'Quicksand', sans-serif; font-size: 10px; color: #333; }
        .gradio-container { font-family: 'Quicksand', sans-serif; font-size: 10px; }
        .chatbot-avatar-user, .chatbot-avatar-bot { border-radius: 50%; width: 36px; height: 36px; object-fit: cover; }
        .chatbot-avatar-user { border: 2px solid #d1eaff; background: #e3f1ff; margin: 0 6px 0 0; }
        .chatbot-avatar-bot { border: 2px solid #ffd580; background: #fff8e1; margin: 0 0 0 6px; }
        .chatbot-message-user { background: linear-gradient(90deg, #e3f1ff 0%, #c9e7ff 100%); color: #222; font-size: 13px; padding: 8px 12px; border-radius: 12px; }
        .chatbot-message-bot { background: linear-gradient(90deg, #fff8e1 0%, #fff3c4 100%); font-size: 10px; padding: 8px 12px; border-radius: 12px; }
        .actions-log { font-family: 'Courier New', monospace; font-size: 10px; background: #f4f4f5; border-radius: 12px; padding: 10px; box-shadow: inset 0 1px 3px rgba(0,0,0,0.05); height: 520px; overflow-y: auto; white-space: pre-wrap; }
        .header-container { position: sticky; top: 0; background: #ffffff; z-index: 10; padding-bottom: 8px; }
    </style>
    """)

    with gr.Column(elem_id="header", elem_classes="header-container"):
        gr.HTML("""
            <div style="display: flex; align-items: center; justify-content: left; width: 100%">
                <img src="https://cdn-icons-png.flaticon.com/512/2490/2490408.png" style="width: 100px; height: 100px; margin-right: 10px;" />
            </div>
            """)
        gr.Markdown("""
        # 👩🏻‍💻 Chatbot 🤖

        - 📄 **Knowledge Base**: Tips, facts, and business insights.
        - 🧠 **Context-Aware**: Handles ongoing conversations.
        - 🪣 **Reset Session** to start from scratch.
        """)

    session_data_state = gr.State(value={"chat_history": []})

    with gr.Row():
        chat_ui = gr.ChatInterface(
            fn=chat_bot_logic,
            additional_inputs=[session_data_state],
            type="messages",
            examples=[["Give me all the available documents"]],
            chatbot=gr.Chatbot(
                label="Conversation",
                avatar_images=(
                    "https://img.icons8.com/fluency/96/user-female-circle.png",
                    "https://img.icons8.com/fluency/96/chatbot.png"),
                height=700,
                show_label=True,
                render_markdown=True,
                autoscroll=True,
                type="messages",
            ),
        )

    chat_ui.additional_outputs = [session_data_state]

if __name__ == "__main__":
    logger.info(f"Gradio version at runtime: {gr.__version__}")
    logger.info("Starting Gradio app with streaming support...")
    logger.info(
        "Chatbot is starting. Access it at the URL provided by Gradio.")
    demo.queue().launch(debug=False, share=False,
                        server_name='0.0.0.0', server_port=8000)
