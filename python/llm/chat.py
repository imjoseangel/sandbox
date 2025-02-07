from typing import Union, List
from pydantic import BaseModel, Field
import requests

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
from langchain_ollama import OllamaLLM as Ollama
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    trim_messages,
)


class WikipediaArticleExporter(BaseModel):
    article: str = Field(
        description="The canonical name of the Wikipedia article")


@tool("wikipedia_text_exporter", args_schema=WikipediaArticleExporter, return_direct=False)
def wikipedia_text_exporter(article: str) -> dict[str, str]:
    '''Fetches the most recent revision for a Wikipedia article in WikiText format.'''
    url = f"https://en.wikipedia.org/w/api.php?action=parse&page={
        article}&prop=wikitext&formatversion=2"

    result = requests.get(url, timeout=60).text
    start = result.find('"wikitext": "{{')
    end = result.find('}</pre></div></div><!--esi')

    result = result[start+12:end-30]

    return {"text": result}


class ChatHistoryManager:
    def __init__(self):
        self.chat_history: List[Union[HumanMessage, SystemMessage]] = [
            SystemMessage(content="You're a helpful assistant.")]

    def append_chat_history(self, user_input, response):
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(SystemMessage(content=response))

    def trim_chat_history(self):
        self.chat_history = trim_messages(
            self.chat_history,
            token_counter=len,  # len will simply count the number of messages rather than tokens
            max_tokens=5,  # allow up to 5 messages
            strategy="last",
            start_on="human",
            include_system=True,
            allow_partial=False,
        )


def invoke(user_input, history_manager: ChatHistoryManager):
    msg = {
        "input": user_input,
        "chat_history": history_manager.chat_history,
    }
    print(f"Input: {msg}")

    response = agent_executor.invoke(msg)
    print(f"Response: {response}")

    history_manager.append_chat_history(user_input, response["output"])
    history_manager.trim_chat_history()
    print(f"History: {history_manager.chat_history}")


tools = [wikipedia_text_exporter]
prompt = hub.pull("hwchase17/react-chat")
llm = Ollama(model="gemma2:9b")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

history = ChatHistoryManager()
invoke("What is the capital of Germany? Do not use a tool.", history)
