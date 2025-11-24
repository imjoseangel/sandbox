# enhanced_server.py
"""
Enhanced MCP Server with multiple tools for RAG-MCP demonstration.

This server provides a variety of tools to showcase how RAG-MCP
can semantically select the most relevant ones.
"""

from mcp.server.fastmcp import FastMCP
import asyncio

# Initialize the MCP server on port 8001
mcp = FastMCP("EnhancedDocServer", port=8001)


@mcp.tool()
def get_document_info(doc_id: int) -> dict:
    """Retrieves detailed information about a document by its ID."""
    print(f"📄 Tool called: get_document_info(doc_id={doc_id})")
    return {
        "doc_id": doc_id,
        "doc_name": f"Document_{doc_id}.pdf",
        "author": "AI Research Team",
        "created_date": "2024-01-15",
        "content_summary": f"This document covers research findings for project {doc_id}.",
        "page_count": 42,
        "status": "published"
    }


@mcp.tool()
def search_documents(query: str, max_results: int = 10) -> dict:
    """Searches for documents matching a text query across all fields."""
    print(f"🔍 Tool called: search_documents(query='{query}', max_results={max_results})")

    # Simulated search results
    results = [
        {
            "doc_id": i,
            "title": f"Document about {query} - Part {i}",
            "relevance_score": 0.95 - (i * 0.1),
            "snippet": f"This document discusses {query} in detail..."
        }
        for i in range(1, min(max_results + 1, 6))
    ]

    return {
        "query": query,
        "total_results": len(results),
        "results": results
    }


@mcp.tool()
def calculate_statistics(numbers: list[float]) -> dict:
    """Calculates statistical metrics (mean, median, std dev) for a list of numbers."""
    print(f"📊 Tool called: calculate_statistics(numbers={numbers})")

    if not numbers:
        return {"error": "No numbers provided"}

    import statistics
    return {
        "count": len(numbers),
        "sum": sum(numbers),
        "mean": statistics.mean(numbers),
        "median": statistics.median(numbers),
        "std_dev": statistics.stdev(numbers) if len(numbers) > 1 else 0,
        "min": min(numbers),
        "max": max(numbers)
    }


@mcp.tool()
def get_user_profile(user_id: int) -> dict:
    """Retrieves user profile information including name, email, and permissions."""
    print(f"👤 Tool called: get_user_profile(user_id={user_id})")
    return {
        "user_id": user_id,
        "username": f"user_{user_id}",
        "email": f"user{user_id}@example.com",
        "full_name": f"User Number {user_id}",
        "role": "researcher" if user_id % 2 == 0 else "viewer",
        "permissions": ["read_documents", "search"] if user_id % 2 == 0 else ["read_documents"]
    }


@mcp.tool()
def create_document_summary(doc_id: int, max_length: int = 200) -> dict:
    """Generates a text summary for a specified document."""
    print(f"📝 Tool called: create_document_summary(doc_id={doc_id}, max_length={max_length})")
    return {
        "doc_id": doc_id,
        "summary": f"This is a {max_length}-character summary of document {doc_id}. "
                   f"The document discusses various aspects of research and development "
                   f"in the field of artificial intelligence and machine learning.",
        "length": max_length,
        "generated_at": "2024-11-17T10:30:00Z"
    }


@mcp.tool()
def convert_units(value: float, from_unit: str, to_unit: str) -> dict:
    """Converts values between different units (length, weight, temperature)."""
    print(f"🔄 Tool called: convert_units(value={value}, from='{from_unit}', to='{to_unit}')")

    # Simple conversion examples
    conversions = {
        ("meters", "feet"): value * 3.28084,
        ("feet", "meters"): value / 3.28084,
        ("kg", "lbs"): value * 2.20462,
        ("lbs", "kg"): value / 2.20462,
        ("celsius", "fahrenheit"): (value * 9/5) + 32,
        ("fahrenheit", "celsius"): (value - 32) * 5/9,
    }

    result = conversions.get((from_unit.lower(), to_unit.lower()), value)

    return {
        "original_value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "converted_value": round(result, 4)
    }


@mcp.tool()
def get_weather_data(location: str, days: int = 7) -> dict:
    """Retrieves weather forecast data for a specified location."""
    print(f"🌤️ Tool called: get_weather_data(location='{location}', days={days})")
    return {
        "location": location,
        "forecast_days": days,
        "current_temperature": 72,
        "conditions": "Partly Cloudy",
        "forecast": [
            {
                "day": i,
                "high": 70 + (i % 5),
                "low": 55 + (i % 3),
                "conditions": ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"][i % 4]
            }
            for i in range(1, days + 1)
        ]
    }


@mcp.tool()
def analyze_document_sentiment(doc_id: int) -> dict:
    """Analyzes the sentiment (positive, negative, neutral) of a document's content."""
    print(f"😊 Tool called: analyze_document_sentiment(doc_id={doc_id})")

    # Simulated sentiment analysis
    sentiments = ["positive", "negative", "neutral"]
    sentiment = sentiments[doc_id % 3]

    return {
        "doc_id": doc_id,
        "overall_sentiment": sentiment,
        "positive_score": 0.7 if sentiment == "positive" else 0.2,
        "negative_score": 0.7 if sentiment == "negative" else 0.1,
        "neutral_score": 0.8 if sentiment == "neutral" else 0.2,
        "confidence": 0.85
    }


@mcp.tool()
def list_recent_documents(limit: int = 10) -> dict:
    """Lists the most recently created or modified documents."""
    print(f"📋 Tool called: list_recent_documents(limit={limit})")
    return {
        "total_count": limit,
        "documents": [
            {
                "doc_id": i,
                "title": f"Recent Document {i}",
                "modified_date": f"2024-11-{17-i:02d}",
                "author": f"Author {i % 5}"
            }
            for i in range(1, limit + 1)
        ]
    }


@mcp.tool()
def translate_text(text: str, source_lang: str, target_lang: str) -> dict:
    """Translates text from one language to another."""
    print(f"🌐 Tool called: translate_text(text='{text[:20]}...', from='{source_lang}', to='{target_lang}')")
    return {
        "original_text": text,
        "source_language": source_lang,
        "target_language": target_lang,
        "translated_text": f"[{target_lang.upper()} translation of: {text}]",
        "confidence": 0.92
    }


async def main():
    print("=" * 80)
    print("🚀 Starting Enhanced MCP Server for RAG-MCP Demo")
    print("=" * 80)
    print(f"\nServer: EnhancedDocServer")
    print(f"Port: 8001")
    print(f"Endpoint: http://localhost:8001/sse")
    print(f"\nAvailable Tools: 10")
    print("  1. get_document_info - Retrieve document details")
    print("  2. search_documents - Search across documents")
    print("  3. calculate_statistics - Calculate statistical metrics")
    print("  4. get_user_profile - Get user information")
    print("  5. create_document_summary - Generate document summaries")
    print("  6. convert_units - Convert between units")
    print("  7. get_weather_data - Get weather forecasts")
    print("  8. analyze_document_sentiment - Analyze sentiment")
    print("  9. list_recent_documents - List recent documents")
    print(" 10. translate_text - Translate text")
    print("\n" + "=" * 80)
    print("Server is ready! Press Ctrl+C to stop.")
    print("=" * 80 + "\n")

    # Run the server
    await mcp.run_sse_async()


if __name__ == "__main__":
    asyncio.run(main())
