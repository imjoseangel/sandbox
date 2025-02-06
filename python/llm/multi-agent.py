from langgraph.graph import StateGraph, END
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import ChatOllama

# Load the document
docs = PyMuPDFLoader("search_rescue_manual.pdf").load()
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=0)
splits = splitter.split_documents(docs)

# Create the vector store
embedding_model = OllamaEmbeddings(model="nomic-embed-text:latest")
vectorstore = Qdrant.from_documents(
    splits, embedding_model, location=":memory:")
retriever = vectorstore.as_retriever()

llm = OllamaLLM(
    model="qwen2.5:3b", temperature=0.03,
    client_kwargs={"verify": False})


functions = ChatOllama(model="qwen2.5:3b", format="json")


@tool
def fetch_info(query: str):
    """Retrieve information from the knowledge base."""
    return retriever.get_relevant_documents(query)


template = '''You are a {role}. Perform your duties professionally.

Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

# Define the agent template
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    MessagesPlaceholder("messages")
])


def create_agent(role):
    return AgentExecutor(
        agent=create_react_agent(
            llm, [fetch_info], agent_prompt.partial(role=role)),
        tools=[fetch_info], verbose=True, handle_parsing_errors=True)


pilot = create_agent("Pilot")
copilot = create_agent("Co-Pilot")
cso = create_agent("Combat Systems Operator")


# Supervisor agent
supervisor_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the supervisor managing Pilot, Co-Pilot, and CSO. Decide who acts next."),
    MessagesPlaceholder("messages")
])
supervisor = supervisor_prompt | functions

# Workflow graph


class MissionState(dict):
    messages: list
    next_agent: str


workflow = StateGraph(MissionState)
workflow.add_node("Pilot", lambda state: pilot.invoke(state))
workflow.add_node("Co-Pilot", lambda state: copilot.invoke(state))
workflow.add_node("CSO", lambda state: cso.invoke(state))
workflow.add_node("Supervisor", supervisor)


workflow.add_edge("Supervisor", "Pilot")
workflow.add_edge("Supervisor", "Co-Pilot")
workflow.add_edge("Supervisor", "CSO")
workflow.add_edge("Pilot", "Supervisor")
workflow.add_edge("Co-Pilot", "Supervisor")
workflow.add_edge("CSO", "Supervisor")
workflow.set_entry_point("Supervisor")

chain = workflow.compile()

scenario = "Mission: Locate the missing SS Meridian in the North Atlantic."

messages = [scenario]
state = {"messages": messages}
while True:
    result = chain.invoke(state)
    if END in result:
        break
    state["messages"].extend(result["messages"])
    print("\n".join(result["messages"]))
