# server.py
from mcp.server.fastmcp import FastMCP
import asyncio

# Initialize the MCP server on port 8001
mcp = FastMCP("SimpleDocServer", port=8001)

@mcp.tool()
def get_document_info(doc_id: int) -> dict:
    """Gets fake document information for a given document ID."""
    print(f"--- Server: Tool 'get_document_info' called with id: {doc_id} ---")
    return {
        "doc_id": doc_id,
        "doc_name": f"Sample Document {doc_id}",
        "author": "AI Engineer",
        "content_summary": "This is a sample document about MCP and LlamaIndex."
    }

async def main():
    print("🚀 Starting simple MCP server on http://localhost:8001")
    # We use run_sse_async for HTTP-based communication
    await mcp.run_sse_async()

if __name__ == "__main__":
    asyncio.run(main())
