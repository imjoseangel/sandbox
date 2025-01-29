from llama_index.llms.ollama import Ollama
from llama_index.core import Settings, SimpleDirectoryReader, SummaryIndex, VectorStoreIndex
from llama_index.core.agent import AgentRunner, FunctionCallingAgentWorker
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import QueryEngineTool
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# load lora_paper.pdf documents
documents = SimpleDirectoryReader(
    input_files=["./datasets/lora_paper.pdf"]).load_data()


# chunk_size of 1024 is a good default value
splitter = SentenceSplitter(chunk_size=1024)
# Create nodes from documents
nodes = splitter.get_nodes_from_documents(documents)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5")
Settings.llm = Ollama(model="qwen2.5-coder", request_timeout=120.0,
                      temperature=0.0, context_window=2048)

llm = Ollama(model="qwen2.5-coder", request_timeout=120.0,
             temperature=0.0, context_window=2048)

summary_index = SummaryIndex(nodes)
vector_index = VectorStoreIndex(nodes)
summary_query_engine = summary_index.as_query_engine(
    response_mode="tree_summarize", use_async=True, )
vector_query_engine = vector_index.as_query_engine()

summary_tool = QueryEngineTool.from_defaults(
    query_engine=summary_query_engine,
    description=(
        "Useful for summarization questions related to the Lora paper."
    ),
)

vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description=(
        "Useful for retrieving specific context from the the Lora paper."
    ),
)

agent_worker = FunctionCallingAgentWorker.from_tools(
    tools=[vector_tool, summary_tool],
    llm=llm,
    verbose=True
)
agent = AgentRunner(agent_worker)

response = agent.query(
    "Explain to me what is Lora and why it's being used. Are existing solutions not good enough?"
)

response = agent.chat(
    "Explain to me what is Lora and why it's being used. Are existing solutions not good enough?"
)

print(str(response))

response = agent.chat(
    "What was my last question to you?"
)

print(str(response))
