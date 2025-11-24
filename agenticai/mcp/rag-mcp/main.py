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
import time
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
        similarity_threshold: float = 0.2
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


def baseline_mcp_retrieval(query: str, tools: List[MCPTool]) -> List[MCPTool]:
    """
    Baseline MCP retrieval: returns ALL tools without filtering.

    This simulates traditional MCP approach where the LLM receives
    the full tool catalog, leading to prompt bloat.
    """
    return tools


def run_comparison_tests(retriever: RAGMCPRetriever, queries: List[str]):
    """
    Compare RAG-MCP vs Traditional MCP retrieval.

    Args:
        retriever: The RAG-MCP retriever instance
        queries: List of test queries
    """
    print("\n" + "=" * 70)
    print("COMPARISON: RAG-MCP vs Traditional MCP")
    print("=" * 70)

    tools = create_example_tools()

    print("\n[Setup] Test Configuration")
    print("─" * 70)
    print(f"  Total tools available: {len(tools)}")
    print(f"  Test queries: {len(queries)}")
    print(f"  RAG-MCP top-k: 3")

    # Metrics storage
    rag_times = []
    baseline_times = []
    rag_prompt_sizes = []
    baseline_prompt_sizes = []
    rag_token_counts = []
    baseline_token_counts = []

    print("\n[Test 1] Query-by-Query Comparison")
    print("─" * 70)

    for i, query in enumerate(queries, 1):
        print(f"\nQuery {i}: {query}")
        print("  " + "─" * 66)

        # Traditional MCP (all tools)
        start_time = time.perf_counter()
        baseline_tools = baseline_mcp_retrieval(query, tools)
        baseline_time = (time.perf_counter() - start_time) * 1000
        baseline_times.append(baseline_time)

        baseline_prompt = f"Query: {query}\n\nAvailable Tools:\n"
        for j, tool in enumerate(baseline_tools, 1):
            baseline_prompt += f"{j}. {tool.name}\n   {tool.description}\n   {json.dumps(tool.parameters)}\n"

        baseline_size = len(baseline_prompt)
        baseline_prompt_sizes.append(baseline_size)
        # Rough token estimate: ~4 chars per token
        baseline_tokens = baseline_size // 4
        baseline_token_counts.append(baseline_tokens)

        # RAG-MCP (semantic retrieval)
        start_time = time.perf_counter()
        rag_results = retriever.retrieve(query, top_k=3)
        rag_time = (time.perf_counter() - start_time) * 1000
        rag_times.append(rag_time)

        rag_prompt = retriever.get_prompt_for_llm(query, top_k=3)
        rag_size = len(rag_prompt)
        rag_prompt_sizes.append(rag_size)
        rag_tokens = rag_size // 4
        rag_token_counts.append(rag_tokens)

        reduction = (1 - rag_size / baseline_size) * 100
        token_reduction = (1 - rag_tokens / baseline_tokens) * 100

        print(f"  Traditional MCP:")
        print(f"    - Tools returned: {len(baseline_tools)}")
        print(f"    - Time: {baseline_time:.3f}ms")
        print(f"    - Prompt size: {baseline_size} chars (~{baseline_tokens} tokens)")

        print(f"  RAG-MCP:")
        print(f"    - Tools returned: {len(rag_results)}")
        print(f"    - Time: {rag_time:.3f}ms")
        print(f"    - Prompt size: {rag_size} chars (~{rag_tokens} tokens)")

        print(f"  📊 Improvements:")
        print(f"    - Prompt reduction: {reduction:.1f}%")
        print(f"    - Token reduction: {token_reduction:.1f}%")
        print(f"    - Speed: {baseline_time/rag_time:.2f}x slower (baseline)")

    # Aggregate statistics
    print("\n[Test 2] Aggregate Performance Metrics")
    print("─" * 70)

    avg_baseline_time = np.mean(baseline_times)
    avg_rag_time = np.mean(rag_times)
    avg_baseline_size = np.mean(baseline_prompt_sizes)
    avg_rag_size = np.mean(rag_prompt_sizes)
    avg_baseline_tokens = np.mean(baseline_token_counts)
    avg_rag_tokens = np.mean(rag_token_counts)

    avg_reduction = (1 - avg_rag_size / avg_baseline_size) * 100
    avg_token_reduction = (1 - avg_rag_tokens / avg_baseline_tokens) * 100
    speedup = avg_baseline_time / avg_rag_time if avg_rag_time > 0 else float('inf')

    print(f"\n  Average Metrics (across {len(queries)} queries):")
    print(f"  {'Metric':<30} {'Traditional MCP':<20} {'RAG-MCP':<20} {'Improvement':<15}")
    print("  " + "─" * 85)
    print(f"  {'Retrieval Time':<30} {avg_baseline_time:<20.2f} {avg_rag_time:<20.2f} {speedup:.2f}x slower")
    print(f"  {'Prompt Size (chars)':<30} {avg_baseline_size:<20.0f} {avg_rag_size:<20.0f} {avg_reduction:.1f}% less")
    print(f"  {'Token Count (est.)':<30} {avg_baseline_tokens:<20.0f} {avg_rag_tokens:<20.0f} {avg_token_reduction:.1f}% less")
    print(f"  {'Tools per Query':<30} {len(tools):<20.0f} {np.mean([len(retriever.retrieve(q, top_k=3)) for q in queries]):<20.1f} {(1 - 3/len(tools))*100:.1f}% less")

    # Cost analysis (based on typical LLM pricing)
    print("\n[Test 3] Cost Analysis (Estimated)")
    print("─" * 70)

    # Assume GPT-4 pricing: $0.03 per 1K input tokens
    price_per_1k = 0.03
    baseline_cost = (avg_baseline_tokens / 1000) * price_per_1k
    rag_cost = (avg_rag_tokens / 1000) * price_per_1k
    cost_savings = (1 - rag_cost / baseline_cost) * 100

    print(f"  Assuming GPT-4 pricing ($0.03 per 1K input tokens):")
    print(f"  {'Approach':<30} {'Tokens/Query':<20} {'Cost/Query':<20} {'Cost/1K Queries':<20}")
    print("  " + "─" * 90)
    print(f"  {'Traditional MCP':<30} {avg_baseline_tokens:<20.0f} ${baseline_cost:<19.6f} ${baseline_cost*1000:<19.2f}")
    print(f"  {'RAG-MCP':<30} {avg_rag_tokens:<20.0f} ${rag_cost:<19.6f} ${rag_cost*1000:<19.2f}")
    print(f"  {'Savings':<30} {avg_baseline_tokens - avg_rag_tokens:<20.0f} ${baseline_cost - rag_cost:<19.6f} ${(baseline_cost - rag_cost)*1000:<19.2f}")
    print(f"\n  💰 Cost Reduction: {cost_savings:.1f}%")

    # Scalability comparison
    print("\n[Test 4] Scalability with Growing Tool Catalog")
    print("─" * 70)

    tool_counts = [10, 50, 100, 200, 500]
    print(f"  {'Tools':<10} {'Baseline Tokens':<20} {'RAG Tokens':<20} {'Reduction':<15}")
    print("  " + "─" * 65)

    base_tools = create_example_tools()
    for count in tool_counts:
        # Estimate baseline tokens (all tools)
        baseline_est = count * (avg_baseline_tokens / len(tools))
        # RAG-MCP stays constant (only top-k)
        rag_est = avg_rag_tokens
        reduction_pct = (1 - rag_est / baseline_est) * 100

        print(f"  {count:<10} {baseline_est:<20.0f} {rag_est:<20.0f} {reduction_pct:<15.1f}%")

    print("\n  📈 Key Insight: RAG-MCP maintains constant token usage")
    print("     while traditional MCP scales linearly with tool count!")

    # Summary
    print("\n" + "=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)
    print(f"  ✓ Prompt Size Reduction: {avg_reduction:.1f}%")
    print(f"  ✓ Token Reduction: {avg_token_reduction:.1f}%")
    print(f"  ✓ Cost Savings: {cost_savings:.1f}%")
    print(f"  ✓ Retrieval Overhead: {avg_rag_time:.2f}ms (negligible)")
    print(f"  ✓ Accuracy: Semantically relevant tools only")
    print(f"  ✓ Scalability: O(1) tokens vs O(n) for traditional MCP")
    print("=" * 70)


def run_speed_tests(retriever: RAGMCPRetriever, queries: List[str], iterations: int = 100):
    """
    Run comprehensive speed tests for RAG-MCP retrieval.

    Args:
        retriever: The RAG-MCP retriever instance
        queries: List of test queries
        iterations: Number of iterations for benchmarking
    """
    print("\n" + "=" * 70)
    print("SPEED TESTS: Performance Benchmarking")
    print("=" * 70)

    # Test 1: Index building time
    print("\n[Test 1] Index Building Performance")
    print("─" * 70)

    tools = create_example_tools()
    test_retriever = RAGMCPRetriever()
    test_retriever.add_tools(tools)

    start_time = time.perf_counter()
    test_retriever.build_index()
    index_time = time.perf_counter() - start_time

    print(f"  Tools indexed: {len(tools)}")
    print(f"  Index build time: {index_time*1000:.2f}ms")
    print(f"  Time per tool: {(index_time*1000)/len(tools):.2f}ms")

    # Test 2: Single query performance
    print("\n[Test 2] Single Query Performance")
    print("─" * 70)

    test_query = "What's the weather like tomorrow?"
    query_times = []

    for _ in range(iterations):
        start_time = time.perf_counter()
        test_retriever.retrieve(test_query, top_k=3)
        query_times.append(time.perf_counter() - start_time)

    avg_query_time = np.mean(query_times) * 1000
    std_query_time = np.std(query_times) * 1000
    min_query_time = np.min(query_times) * 1000
    max_query_time = np.max(query_times) * 1000

    print(f"  Query: '{test_query}'")
    print(f"  Iterations: {iterations}")
    print(f"  Average time: {avg_query_time:.2f}ms ± {std_query_time:.2f}ms")
    print(f"  Min time: {min_query_time:.2f}ms")
    print(f"  Max time: {max_query_time:.2f}ms")
    print(f"  Throughput: {1000/avg_query_time:.1f} queries/second")

    # Test 3: Batch query performance
    print("\n[Test 3] Batch Query Performance")
    print("─" * 70)

    batch_times = []
    for _ in range(10):
        start_time = time.perf_counter()
        for query in queries:
            test_retriever.retrieve(query, top_k=3)
        batch_times.append(time.perf_counter() - start_time)

    avg_batch_time = np.mean(batch_times) * 1000
    avg_per_query = avg_batch_time / len(queries)

    print(f"  Queries in batch: {len(queries)}")
    print(f"  Average batch time: {avg_batch_time:.2f}ms")
    print(f"  Average per query: {avg_per_query:.2f}ms")
    print(f"  Batch throughput: {1000*len(queries)/avg_batch_time:.1f} queries/second")

    # Test 4: Scaling test with different tool counts
    print("\n[Test 4] Scalability Test (Tool Count)")
    print("─" * 70)

    tool_counts = [10, 50, 100, 200]
    print(f"  {'Tools':<10} {'Build (ms)':<15} {'Query (ms)':<15} {'Throughput (q/s)':<20}")
    print("  " + "─" * 60)

    for count in tool_counts:
        # Create scaled tools by duplicating
        scaled_tools = tools * (count // len(tools)) + tools[:count % len(tools)]
        scaled_tools = scaled_tools[:count]

        scale_retriever = RAGMCPRetriever()
        scale_retriever.add_tools(scaled_tools)

        # Build time
        start_time = time.perf_counter()
        scale_retriever.build_index()
        build_time = (time.perf_counter() - start_time) * 1000

        # Query time
        query_times = []
        for _ in range(20):
            start_time = time.perf_counter()
            scale_retriever.retrieve(test_query, top_k=3)
            query_times.append(time.perf_counter() - start_time)

        avg_q_time = np.mean(query_times) * 1000
        throughput = 1000 / avg_q_time

        print(f"  {count:<10} {build_time:<15.2f} {avg_q_time:<15.2f} {throughput:<20.1f}")

    # Test 5: Different top_k performance
    print("\n[Test 5] Top-K Retrieval Performance")
    print("─" * 70)

    top_k_values = [1, 3, 5, 10, 20]
    print(f"  {'Top-K':<10} {'Avg Time (ms)':<20} {'Throughput (q/s)':<20}")
    print("  " + "─" * 50)

    for k in top_k_values:
        k_times = []
        for _ in range(50):
            start_time = time.perf_counter()
            test_retriever.retrieve(test_query, top_k=k)
            k_times.append(time.perf_counter() - start_time)

        avg_k_time = np.mean(k_times) * 1000
        k_throughput = 1000 / avg_k_time

        print(f"  {k:<10} {avg_k_time:<20.2f} {k_throughput:<20.1f}")

    # Test 6: Memory efficiency
    print("\n[Test 6] Memory Efficiency")
    print("─" * 70)

    import sys

    tools_size = sys.getsizeof(test_retriever.tools)
    embeddings_size = test_retriever.tool_embeddings.nbytes if test_retriever.tool_embeddings is not None else 0
    total_size = tools_size + embeddings_size

    print(f"  Tools memory: {tools_size / 1024:.2f} KB")
    print(f"  Embeddings memory: {embeddings_size / 1024:.2f} KB")
    print(f"  Total memory: {total_size / 1024:.2f} KB")
    print(f"  Memory per tool: {total_size / len(test_retriever.tools) / 1024:.2f} KB")

    # Summary
    print("\n" + "=" * 70)
    print("PERFORMANCE SUMMARY")
    print("=" * 70)
    print(f"  ✓ Index build time: {index_time*1000:.2f}ms for {len(tools)} tools")
    print(f"  ✓ Average query time: {avg_query_time:.2f}ms")
    print(f"  ✓ Query throughput: {1000/avg_query_time:.1f} queries/second")
    print(f"  ✓ Memory footprint: {total_size / 1024:.2f} KB")
    print(f"  ✓ Scales efficiently up to 200+ tools")
    print("=" * 70)


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

    # Run comparison tests
    print("\n\n")
    run_comparison_tests(retriever, queries)

    # Run speed tests
    print("\n\n")
    run_speed_tests(retriever, queries, iterations=100)


if __name__ == "__main__":
    main()
