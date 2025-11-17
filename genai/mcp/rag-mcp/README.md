# RAG-MCP: Retrieval-Augmented Generation for MCP Tool Selection

This project demonstrates the RAG-MCP technique for optimizing tool selection in Model Context Protocol (MCP) servers using semantic retrieval.

## Overview

**RAG-MCP** reduces prompt bloat and improves tool selection accuracy by using semantic similarity to retrieve only the most relevant tools for a given query, instead of passing all available tools to the LLM.

### Key Benefits

- 🎯 **Token Reduction**: >50% reduction in prompt tokens
- 📈 **Scalability**: Constant token usage regardless of tool count
- 🔍 **Better Selection**: Semantically relevant tools only
- 💰 **Cost Savings**: Proportional reduction in API costs

## Files

### Core Implementation

- **`main.py`**: Standalone RAG-MCP demonstration with simulated tools
  - Shows comparison between traditional and RAG-MCP approaches
  - Includes performance benchmarks and scaling tests
  - No external server required

### MCP Server Integration

- **`server.py`**: Simple MCP server with one tool (basic demo)
- **`enhanced_server.py`**: Enhanced MCP server with 10 diverse tools
  - Document management tools
  - User profile tools
  - Utility tools (calculations, conversions, weather)
  - Text processing tools

### Agent Clients

- **`agent_client.py`**: Basic agent client connecting to MCP server
  - Uses all available MCP tools
  - Traditional approach (no RAG)

- **`rag_agent_client.py`**: **RAG-MCP agent client** (NEW!)
  - Combines semantic retrieval with live MCP tools
  - Demonstrates token reduction with real tools
  - Includes comparison between traditional and RAG approaches

## Quick Start

### Option 1: Standalone Demo (No Server Required)

Run the RAG-MCP concept demonstration:

```bash
python main.py
```

This will:
- Create 12 example tools
- Demonstrate semantic tool retrieval
- Run comparison tests
- Show performance benchmarks

### Option 2: MCP Server Integration

#### Step 1: Start the Enhanced MCP Server

In terminal 1:
```bash
python enhanced_server.py
```

You should see:
```
🚀 Starting Enhanced MCP Server for RAG-MCP Demo
Available Tools: 10
Server is ready!
```

#### Step 2: Run the RAG-MCP Agent Client

In terminal 2:
```bash
python rag_agent_client.py
```

This will:
1. Connect to the MCP server
2. Retrieve all available tools
3. Build a semantic index
4. Test RAG-based tool selection with multiple queries
5. Compare traditional MCP vs RAG-MCP approaches

## How It Works

### Traditional MCP Approach

```
User Query → [All 10 Tools] → LLM Agent → Response
              ↑
         Large prompt,
         high token cost
```

### RAG-MCP Approach

```
User Query → Semantic Search → [Top 2-3 Relevant Tools] → LLM Agent → Response
                   ↑                      ↑
            Vector embeddings      Reduced prompt,
                                  lower token cost
```

## Example Output

### RAG Tool Selection

```
Query: "I need to get information about document 42"

🔍 Selecting relevant tools:
  📌 Selected: get_document_info (relevance: 0.8234)
  📌 Selected: search_documents (relevance: 0.6891)

📊 RAG Retrieval Statistics:
   Total tools available: 10
   Tools to be sent to LLM: 2
   Token reduction: ~80%
```

### Comparison Results

```
[Approach 1] Traditional MCP - Using ALL tools
   Tools provided to LLM: 10
   Estimated prompt tokens: ~500

[Approach 2] RAG-MCP - Using SELECTED tools
   Tools provided to LLM: 2
   Estimated prompt tokens: ~100
```

## Configuration

### LLM Settings (in `rag_agent_client.py`)

Using LM Studio:
```python
Settings.llm = OpenAI(
    model="gpt-3.5-turbo",
    api_base="http://localhost:1234/v1",
    api_key="lm-studio",
    is_chat_model=True,
    temperature=0.7
)
```

Using OpenAI:
```python
Settings.llm = OpenAI(
    model="gpt-4o-mini",
    api_key="your-api-key-here",
    temperature=0.7
)
```

### RAG Parameters

```python
# In RAGToolRetriever
top_k = 3  # Number of tools to retrieve
similarity_threshold = 0.2  # Minimum similarity score
```

## Requirements

```bash
pip install llama-index
pip install llama-index-llms-openai
pip install llama-index-tools-mcp
pip install mcp
pip install sentence-transformers
pip install scikit-learn
pip install numpy
```

## Architecture

### RAGToolRetriever Class

The core component that enables RAG-MCP:

```python
class RAGToolRetriever:
    def __init__(self, model_name="all-MiniLM-L6-v2")
    def add_tools(tools: List[BaseTool])
    def retrieve_relevant_tools(query: str, top_k: int = 3)
    def get_statistics(query: str, top_k: int = 3)
```

### Workflow

1. **Index Building**: Tool descriptions are embedded using Sentence Transformers
2. **Query Processing**: User query is embedded using the same model
3. **Similarity Search**: Cosine similarity ranks tools by relevance
4. **Tool Selection**: Top-k tools above threshold are selected
5. **Agent Creation**: LLM agent uses only selected tools

## Performance Metrics

Based on the enhanced server with 10 tools:

| Metric | Traditional MCP | RAG-MCP (top-k=2) | Improvement |
|--------|----------------|-------------------|-------------|
| Tools per query | 10 | 2 | 80% reduction |
| Estimated tokens | ~500 | ~100 | 80% reduction |
| Context bloat | High | Low | Significant |
| Scalability | O(n) | O(k) | Constant |

## Use Cases

1. **Large Tool Catalogs**: When you have 50+ tools and want to reduce context
2. **Cost Optimization**: Reduce API costs for high-volume applications  
3. **Improved Accuracy**: Focus LLM attention on relevant tools only
4. **Multi-domain Tools**: Semantically separate tools by domain/category

## Advanced Features

### Custom Similarity Models

Change the embedding model:
```python
retriever = RAGToolRetriever(model_name="all-mpnet-base-v2")
```

### Dynamic Top-K

Adjust based on query complexity:
```python
def adaptive_top_k(query: str) -> int:
    # More complex queries might need more tools
    return 5 if len(query.split()) > 10 else 3
```

### Tool Caching

Cache embeddings to avoid recomputation:
```python
# Embeddings are automatically cached in the retriever
# Just call add_tools() once at initialization
```

## Troubleshooting

### Connection Errors

If you get connection errors:
1. Make sure `enhanced_server.py` is running
2. Check the port (default: 8001)
3. Verify the URL in client: `http://localhost:8001/sse`

### LM Studio Issues

If using LM Studio:
1. Start LM Studio and load a model
2. Enable the local server (default port: 1234)
3. Update `api_base` if using a different port

### Import Errors

Install missing dependencies:
```bash
pip install sentence-transformers scikit-learn
```

## References

- **Paper**: RAG-MCP: Retrieval-Augmented Generation for MCP Tool Selection (arXiv:2505.03275)
- **Model Context Protocol**: https://modelcontextprotocol.io
- **LlamaIndex**: https://docs.llamaindex.ai

## License

MIT

## Contributing

Contributions welcome! This is a demonstration project showcasing the RAG-MCP technique.
