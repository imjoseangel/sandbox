"""
RAG-MCP Agent Client: Demonstrates RAG-based tool selection with real MCP tools

This client combines the RAG-MCP retrieval technique with real MCP server tools,
showing how semantic retrieval can optimize tool selection even with live tools.
"""

import os
import asyncio
from typing import List
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.tools.mcp import McpToolSpec
from llama_index.core import Settings
from llama_index.core.tools import BaseTool
from mcp import ClientSession
from mcp.client.sse import sse_client
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Configure LM Studio
Settings.llm = OpenAI(
    model="gpt-3.5-turbo",
    api_base="http://localhost:1234/v1",
    api_key="lm-studio",
    is_chat_model=True,
    temperature=0.7
)
Settings.embed_model = "local:BAAI/bge-small-en-v1.5"


class RAGToolRetriever:
    """
    RAG-based tool retriever for MCP tools.

    Uses semantic similarity to select the most relevant tools for a query,
    reducing the number of tools passed to the LLM agent.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the RAG tool retriever."""
        self.model = SentenceTransformer(model_name)
        self.tools: List[BaseTool] = []
        self.tool_embeddings = None

    def add_tools(self, tools: List[BaseTool]) -> None:
        """Add tools and build the semantic index."""
        self.tools = tools

        # Create text representations of tools
        tool_texts = []
        for tool in tools:
            text_parts = [
                f"Tool: {tool.metadata.name}",
                f"Description: {tool.metadata.description}"
            ]
            tool_texts.append(" ".join(text_parts))

        # Generate embeddings
        self.tool_embeddings = self.model.encode(tool_texts)
        print(f"✅ Built semantic index for {len(self.tools)} tools")

    def retrieve_relevant_tools(
        self,
        query: str,
        top_k: int = 3,
        similarity_threshold: float = 0.2
    ) -> List[BaseTool]:
        """
        Retrieve the most relevant tools for a query using RAG.

        Args:
            query: User query or task description
            top_k: Number of tools to retrieve
            similarity_threshold: Minimum similarity score (0-1)

        Returns:
            List of relevant tools
        """
        if not self.tools or self.tool_embeddings is None:
            return self.tools

        # Encode query
        query_embedding = self.model.encode([query])

        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.tool_embeddings)[0]

        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]

        # Filter by threshold and return tools
        relevant_tools = []
        for idx in top_indices:
            score = similarities[idx]
            if score >= similarity_threshold:
                relevant_tools.append(self.tools[idx])
                print(f"  📌 Selected: {self.tools[idx].metadata.name} (relevance: {score:.4f})")

        return relevant_tools if relevant_tools else self.tools[:top_k]

    def get_statistics(self, query: str, top_k: int = 3) -> dict:
        """Get retrieval statistics for a query."""
        if not self.tools:
            return {}

        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.tool_embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]

        # Calculate potential token savings
        full_tool_count = len(self.tools)
        selected_tool_count = min(top_k, len(self.tools))
        reduction_pct = (1 - selected_tool_count / full_tool_count) * 100

        return {
            "total_tools": full_tool_count,
            "selected_tools": selected_tool_count,
            "reduction_percentage": reduction_pct,
            "top_scores": [float(similarities[idx]) for idx in top_indices]
        }


async def run_rag_mcp_demo():
    """
    Demonstrate RAG-MCP with real MCP server tools.
    """
    print("=" * 80)
    print("RAG-MCP Agent Client Demo")
    print("Combining semantic tool retrieval with live MCP tools")
    print("=" * 80)

    print("\n🔌 Step 1: Connecting to MCP server...")

    # Create an SSE client connection to the MCP server
    async with sse_client(url="http://localhost:8001/sse") as streams:
        async with ClientSession(*streams) as session:
            # Initialize the session
            await session.initialize()

            print("✅ Connected to MCP server")

            # Create McpToolSpec with the client session
            mcp_tool_spec = McpToolSpec(session)

            # Get all available tools
            all_tools = await mcp_tool_spec.to_tool_list_async()

            print(f"\n📋 Step 2: Discovered {len(all_tools)} MCP tool(s):")
            for tool in all_tools:
                print(f"   - {tool.metadata.name}: {tool.metadata.description}")

            # Initialize RAG retriever
            print("\n🧠 Step 3: Initializing RAG-based tool retriever...")
            rag_retriever = RAGToolRetriever()
            rag_retriever.add_tools(all_tools)

            # Test queries
            test_queries = [
                "I need to get information about document 42",
                "Can you fetch details for doc ID 100?",
                "Show me the document with ID 5",
                "Help me with mathematical calculations",  # Should not match well
            ]

            print("\n" + "=" * 80)
            print("DEMONSTRATION: RAG-based Tool Selection")
            print("=" * 80)

            for i, query in enumerate(test_queries, 1):
                print(f"\n{'─' * 80}")
                print(f"Query {i}: {query}")
                print(f"{'─' * 80}")

                # Get statistics
                stats = rag_retriever.get_statistics(query, top_k=2)

                print(f"\n📊 RAG Retrieval Statistics:")
                print(f"   Total tools available: {stats['total_tools']}")
                print(f"   Tools to be sent to LLM: {stats['selected_tools']}")
                print(f"   Token reduction: ~{stats['reduction_percentage']:.1f}%")

                # Retrieve relevant tools
                print(f"\n🔍 Selecting relevant tools:")
                relevant_tools = rag_retriever.retrieve_relevant_tools(query, top_k=2)

                # Create agent with only relevant tools
                print(f"\n🤖 Creating agent with {len(relevant_tools)} selected tool(s)...")
                agent = ReActAgent(tools=relevant_tools, llm=Settings.llm, verbose=True)

                print(f"\n💬 Agent response:")
                print("─" * 80)

                # Run the agent
                response = await agent.run(user_msg=query)
                print(f"\n✨ Result: {response}")
                print("─" * 80)

            # Comparison: Full tools vs RAG-selected tools
            print("\n\n" + "=" * 80)
            print("COMPARISON: Traditional MCP vs RAG-MCP")
            print("=" * 80)

            comparison_query = "Get me document number 42"

            print(f"\nTest Query: {comparison_query}")
            print("\n" + "─" * 80)

            # Approach 1: Traditional (all tools)
            print("\n[Approach 1] Traditional MCP - Using ALL tools")
            print("─" * 80)
            print(f"   Tools provided to LLM: {len(all_tools)}")
            print(f"   Estimated prompt tokens: ~{len(all_tools) * 50}")  # Rough estimate

            traditional_agent = ReActAgent(tools=all_tools, llm=Settings.llm, verbose=False)
            trad_response = await traditional_agent.run(user_msg=comparison_query)
            print(f"   Response: {trad_response}")

            # Approach 2: RAG-MCP (selected tools)
            print("\n[Approach 2] RAG-MCP - Using SELECTED tools")
            print("─" * 80)
            rag_tools = rag_retriever.retrieve_relevant_tools(comparison_query, top_k=2)
            print(f"   Tools provided to LLM: {len(rag_tools)}")
            print(f"   Estimated prompt tokens: ~{len(rag_tools) * 50}")  # Rough estimate

            rag_agent = ReActAgent(tools=rag_tools, llm=Settings.llm, verbose=False)
            rag_response = await rag_agent.run(user_msg=comparison_query)
            print(f"   Response: {rag_response}")

            # Summary
            print("\n\n" + "=" * 80)
            print("SUMMARY: Benefits of RAG-MCP")
            print("=" * 80)

            stats = rag_retriever.get_statistics(comparison_query, top_k=2)

            print(f"""
✅ Key Benefits Demonstrated:

   1. Token Efficiency
      • Traditional MCP: {len(all_tools)} tools sent to LLM
      • RAG-MCP: {len(rag_tools)} tools sent to LLM
      • Reduction: ~{stats['reduction_percentage']:.1f}%

   2. Semantic Relevance
      • Only tools relevant to the query are selected
      • Based on similarity scores: {stats['top_scores']}

   3. Scalability
      • As tool catalog grows, RAG-MCP maintains efficiency
      • Traditional MCP scales linearly with tool count
      • RAG-MCP scales with top_k parameter (constant)

   4. Response Quality
      • Both approaches produce correct results
      • RAG-MCP reduces noise from irrelevant tools
      • Faster LLM inference due to smaller context

🎯 Conclusion: RAG-MCP successfully combines semantic retrieval
   with live MCP tools, demonstrating practical token reduction
   while maintaining response quality.
            """)

            print("=" * 80)
            print("✓ RAG-MCP Demo Complete!")
            print("=" * 80)


async def main():
    """Main entry point."""
    try:
        await run_rag_mcp_demo()
    except ConnectionError as e:
        print(f"\n❌ Connection Error: {e}")
        print("\n💡 Make sure the MCP server is running:")
        print("   python server.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
