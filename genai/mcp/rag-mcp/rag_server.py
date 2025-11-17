import os
import sys
from llama_index.core import VectorStoreIndex, Document
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from mcp.server.fastmcp import FastMCP
import asyncio

Settings.llm = OpenAI(
    model="gpt-3.5-turbo",
    api_base="http://localhost:1234/v1",
    api_key="lm-studio",
    is_chat_model=True,
    temperature=0.7
)
Settings.embed_model = "local:BAAI/bge-small-en-v1.5"

# Redirect print statements to stderr to avoid interfering with JSON-RPC on stdout
print("📚 Creating and indexing documents for RAG pipeline...", file=sys.stderr)
# Create some dummy documents
docs = [
    Document(text="The Model Context Protocol (MCP) is an open standard for AI tool use."),
    Document(text="LlamaIndex is a data framework for building LLM applications."),
    Document(text="Sam McLeod built an MCP server for benchmarking vLLM deployments.")
]
index = VectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine()
print("✅ RAG pipeline is ready.", file=sys.stderr)

# Initialize the MCP server on port 8002
mcp = FastMCP("LlamaIndexRAGServer", port=8002)

@mcp.tool()
def query_my_documents(query: str) -> str:
    """
    Searches private documents about LlamaIndex and MCP to answer a question.
    Use this for any questions about these specific topics.
    """
    print(f"--- RAG Server: Tool 'query_my_documents' called with query: '{query}' ---", file=sys.stderr)
    response = query_engine.query(query)
    return str(response)

async def main():
    print("🚀 Starting LlamaIndex RAG MCP server on http://localhost:8002", file=sys.stderr)
    await mcp.run_sse_async()

if __name__ == "__main__":
    # This combines the setup and running logic
    asyncio.run(main())
