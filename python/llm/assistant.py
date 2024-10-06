from rich.pretty import pprint
from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from phi.llm.ollama import OllamaTools

print("============= llama3 finance assistant =============")
assistant = Assistant(
    llm=OllamaTools(model="llama3.2"),
    tools=[DuckDuckGo()],
    show_tool_calls=True,
)
assistant.cli_app("Share a quick healthy breakfast recipe.", max_results=1, markdown=True, stream=False)
print("\n-*- Metrics:")
pprint(assistant.llm.metrics)
