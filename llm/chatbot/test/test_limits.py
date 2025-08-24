#!/usr/bin/env python3
"""
Test script to find optimal document size limit for LLM processing.
Tests different character limits until failure.
"""

import os
import tempfile
import shutil
from llama_index.core import Settings, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama

# LLM Configuration (same as main.py)
MODEL = "gpt-oss:20b"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

Settings.llm = Ollama(
    model=MODEL,
    base_url=OLLAMA_HOST,
    thinking=False,
    temperature=0.0,
    max_retries=5,
    context_window=8096,
)


def load_document_with_limit(pdf_path, char_limit):
    """Load document with specified character limit."""
    try:
        temp_dir = tempfile.mkdtemp()
        filename = os.path.basename(pdf_path)
        dest_path = os.path.join(temp_dir, filename)
        shutil.copy2(pdf_path, dest_path)

        documents = SimpleDirectoryReader(temp_dir).load_data()

        if documents:
            doc_text = documents[0].text.strip()
            content = doc_text[:char_limit] + \
                "..." if len(doc_text) > char_limit else doc_text
        else:
            content = ""

        shutil.rmtree(temp_dir, ignore_errors=True)
        return content
    except Exception as e:
        print(f"Error loading document: {e}")
        return ""


def test_llm_with_content(content, question="Who is the author?"):
    """Test LLM with given content and question."""
    try:
        enhanced_msg = f"Based on the uploaded document: {question}\n\n--- DOCUMENT CONTENT ---\n{content}"

        # Get LLM response
        response = Settings.llm.complete(enhanced_msg)

        return {
            "success": True,
            "response": str(response),
            "content_length": len(content),
            "message_length": len(enhanced_msg)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "content_length": len(content),
            "message_length": len(enhanced_msg) if 'enhanced_msg' in locals() else 0
        }


def run_tests():
    """Run tests with different character limits."""
    pdf_path = "/Users/imjoseangel/Downloads/PDF/The_Imitation_Game.pdf"

    if not os.path.exists(pdf_path):
        print(f"PDF not found: {pdf_path}")
        return

    # Test different character limits
    limits = [1000, 1500, 2000, 2500, 3000,
              3500, 4000, 4500, 5000, 6000, 7000, 8000]

    print("Testing different document size limits...\n")
    print(f"{'Limit':<6} {'Content':<8} {'Message':<8} {'Status':<8} {'Response Preview'}")
    print("-" * 80)

    for limit in limits:
        print(f"{limit:<6}", end=" ")

        # Load document with limit
        content = load_document_with_limit(pdf_path, limit)

        if not content:
            print(f"{'N/A':<8} {'N/A':<8} {'LOAD_ERR':<8} Failed to load document")
            continue

        # Test with LLM
        result = test_llm_with_content(content)

        content_len = result['content_length']
        msg_len = result['message_length']

        print(f"{content_len:<8} {msg_len:<8}", end=" ")

        if result['success']:
            response_preview = result['response'][:50].replace(
                '\n', ' ') + "..."
            print(f"{'SUCCESS':<8} {response_preview}")
        else:
            error_preview = result['error'][:50].replace('\n', ' ') + "..."
            print(f"{'FAILED':<8} {error_preview}")

        # If we hit an error, break and show details
        if not result['success']:
            print(f"\nFAILED at limit {limit}")
            print(f"Content length: {content_len}")
            print(f"Message length: {msg_len}")
            print(f"Error: {result['error']}")
            break

    print("\nTest completed!")


if __name__ == "__main__":
    run_tests()
