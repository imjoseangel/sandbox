"""
RAG-MCP: Retrieval-Augmented Generation for MCP Tool Selection

This implementation demonstrates the RAG-MCP technique from arXiv:2505.03275
to mitigate prompt bloat in LLM tool selection by using semantic retrieval
to identify relevant tools before engaging the LLM.

Key benefits:
- Reduces prompt tokens by >50%
- Improves tool selection accuracy (43.13% vs 13.62% baseline)
- Enables scalable tool integration
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class MCPTool:
    """Represents an MCP tool with its metadata."""
    name: str
    description: str
    parameters: Dict[str, Any]
    category: Optional[str] = None
    examples: Optional[List[str]] = None


class RAGMCPRetriever:
    """
    RAG-MCP Retriever for semantic tool selection.

    Uses embeddings to find the most relevant tools for a given query,
    reducing prompt bloat and improving selection accuracy.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the RAG-MCP retriever.

        Args:
            model_name: Sentence transformer model for embeddings
        """
        self.model = SentenceTransformer(model_name)
        self.tools: List[MCPTool] = []
        self.tool_embeddings: Optional[np.ndarray] = None
        self.index_built = False

    def add_tool(self, tool: MCPTool) -> None:
        """Add a tool to the retriever."""
        self.tools.append(tool)
        self.index_built = False

    def add_tools(self, tools: List[MCPTool]) -> None:
        """Add multiple tools to the retriever."""
        self.tools.extend(tools)
        self.index_built = False

    def build_index(self) -> None:
        """Build the semantic index for all tools."""
        if not self.tools:
            raise ValueError("No tools available to index")

        tool_texts = []
        for tool in self.tools:
            text_parts = [
                f"Tool: {tool.name}",
                f"Description: {tool.description}"
            ]

            if tool.category:
                text_parts.append(f"Category: {tool.category}")

            if tool.examples:
                text_parts.append(f"Examples: {' '.join(tool.examples)}")

            tool_texts.append(" ".join(text_parts))

        # Generate embeddings
        self.tool_embeddings = self.model.encode(tool_texts)
        self.index_built = True
        print(f"Index built with {len(self.tools)} tools")

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.3
    ) -> List[tuple[MCPTool, float]]:
        """
        Retrieve the most relevant tools for a query.

        Args:
            query: User query or task description
            top_k: Number of tools to retrieve
            similarity_threshold: Minimum similarity score (0-1)

        Returns:
            List of (tool, similarity_score) tuples
        """
        if not self.index_built:
            self.build_index()

        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.tool_embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = similarities[idx]
            if score >= similarity_threshold:
                results.append((self.tools[idx], float(score)))

        return results

    def retrieve_tools_only(self, query: str, top_k: int = 5) -> List[MCPTool]:
        """Retrieve only the tool objects without scores."""
        results = self.retrieve(query, top_k)
        return [tool for tool, _ in results]

    def get_prompt_for_llm(
        self,
        query: str,
        top_k: int = 5,
        include_scores: bool = False
    ) -> str:
        """
        Generate an optimized prompt with only relevant tools.

        This is the key RAG-MCP benefit: drastically reduced prompt size.
        """
        results = self.retrieve(query, top_k)

        if not results:
            return f"Query: {query}\n\nNo relevant tools found."

        prompt_parts = [f"Query: {query}\n"]
        prompt_parts.append("Available Tools:")

        for i, (tool, score) in enumerate(results, 1):
            tool_desc = f"\n{i}. {tool.name}"
            if include_scores:
                tool_desc += f" (relevance: {score:.2f})"
            tool_desc += f"\n   Description: {tool.description}"
            tool_desc += f"\n   Parameters: {json.dumps(tool.parameters, indent=6)}"
            prompt_parts.append(tool_desc)

        return "\n".join(prompt_parts)

    def get_stats(self) -> Dict[str, Any]:
        """Get retriever statistics."""
        return {
            "total_tools": len(self.tools),
            "index_built": self.index_built,
            "model": self.model.get_sentence_embedding_dimension()
        }


def create_example_tools() -> List[MCPTool]:
    """Create example MCP tools for demonstration."""
    return [
        MCPTool(
            name="web_search",
            description="Search the web for information using a search engine",
            parameters={"query": "string", "max_results": "int"},
            category="information_retrieval",
            examples=["search for recent news", "find information about"]
        ),
        MCPTool(
            name="file_read",
            description="Read the contents of a file from the filesystem",
            parameters={"file_path": "string", "encoding": "string"},
            category="file_operations",
            examples=["read file", "open file", "view file contents"]
        ),
        MCPTool(
            name="file_write",
            description="Write content to a file on the filesystem",
            parameters={"file_path": "string", "content": "string", "mode": "string"},
            category="file_operations",
            examples=["write to file", "save file", "create file"]
        ),
        MCPTool(
            name="calculate",
            description="Perform mathematical calculations and evaluations",
            parameters={"expression": "string"},
            category="computation",
            examples=["calculate", "compute", "evaluate math expression"]
        ),
        MCPTool(
            name="send_email",
            description="Send an email message to recipients",
            parameters={"to": "list[string]", "subject": "string", "body": "string"},
            category="communication",
            examples=["send email", "email someone", "compose message"]
        ),
        MCPTool(
            name="database_query",
            description="Execute SQL queries on a database",
            parameters={"query": "string", "database": "string"},
            category="data_access",
            examples=["query database", "run SQL", "fetch data from database"]
        ),
        MCPTool(
            name="image_generate",
            description="Generate images from text descriptions using AI",
            parameters={"prompt": "string", "size": "string", "style": "string"},
            category="content_generation",
            examples=["generate image", "create picture", "draw from description"]
        ),
        MCPTool(
            name="text_summarize",
            description="Summarize long text documents into concise summaries",
            parameters={"text": "string", "max_length": "int"},
            category="text_processing",
            examples=["summarize text", "create summary", "condense document"]
        ),
        MCPTool(
            name="weather_forecast",
            description="Get weather forecast for a specific location",
            parameters={"location": "string", "days": "int"},
            category="information_retrieval",
            examples=["check weather", "weather forecast", "what's the weather"]
        ),
        MCPTool(
            name="translate",
            description="Translate text from one language to another",
            parameters={"text": "string", "source_lang": "string", "target_lang": "string"},
            category="text_processing",
            examples=["translate text", "convert language", "translation"]
        ),
        MCPTool(
            name="code_execute",
            description="Execute code in a sandboxed environment",
            parameters={"code": "string", "language": "string"},
            category="computation",
            examples=["run code", "execute script", "evaluate code"]
        ),
        MCPTool(
            name="calendar_event",
            description="Create or manage calendar events",
            parameters={"title": "string", "start_time": "datetime", "duration": "int"},
            category="productivity",
            examples=["schedule meeting", "create event", "add to calendar"]
        ),
    ]


def main():
    """Demonstrate RAG-MCP tool retrieval."""
    print("=" * 70)
    print("RAG-MCP: Retrieval-Augmented Generation for MCP Tool Selection")
    print("Based on arXiv:2505.03275")
    print("=" * 70)

    print("\n[1] Initializing RAG-MCP Retriever...")
    retriever = RAGMCPRetriever()

    print("[2] Adding MCP tools...")
    tools = create_example_tools()
    retriever.add_tools(tools)

    print("[3] Building semantic index...")
    retriever.build_index()

    print(f"\nRetriever Stats: {retriever.get_stats()}")

    queries = [
        "I need to find information about climate change",
        "Help me write data to a file",
        "Can you calculate the square root of 144?",
        "I want to create an image of a sunset",
        "What's the weather like tomorrow?",
    ]

    print("\n" + "=" * 70)
    print("DEMONSTRATION: Tool Retrieval with RAG-MCP")
    print("=" * 70)

    for i, query in enumerate(queries, 1):
        print(f"\n{'─' * 70}")
        print(f"Query {i}: {query}")
        print(f"{'─' * 70}")

        results = retriever.retrieve(query, top_k=3)

        print(f"\nTop-{len(results)} Retrieved Tools (with relevance scores):")
        for rank, (tool, score) in enumerate(results, 1):
            print(f"  {rank}. {tool.name:<20} | Relevance: {score:.4f}")
            print(f"     {tool.description}")

        full_prompt_size = sum(
            len(f"{t.name} {t.description} {json.dumps(t.parameters)}")
            for t in tools
        )
        rag_prompt_size = sum(
            len(f"{t.name} {t.description} {json.dumps(t.parameters)}")
            for t, _ in results
        )
        reduction = (1 - rag_prompt_size / full_prompt_size) * 100

        print(f"\n  📊 Prompt Size Reduction: {reduction:.1f}%")
        print(f"     Full prompt: ~{full_prompt_size} chars")
        print(f"     RAG-MCP:     ~{rag_prompt_size} chars")

    print("\n" + "=" * 70)
    print("EXAMPLE: Optimized Prompt for LLM")
    print("=" * 70)

    example_query = "I need to analyze data from a database and create a summary"
    print(f"\nQuery: {example_query}\n")

    optimized_prompt = retriever.get_prompt_for_llm(
        example_query,
        top_k=3,
        include_scores=True
    )
    print(optimized_prompt)

    print("\n" + "=" * 70)
    print("✓ RAG-MCP Demo Complete")
    print("=" * 70)
    print("\nKey Benefits:")
    print("  • Reduced prompt bloat (>50% token reduction)")
    print("  • Improved tool selection accuracy")
    print("  • Scalable to hundreds of tools")
    print("  • Semantic understanding of tool relevance")


if __name__ == "__main__":
    main()
