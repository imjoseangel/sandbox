#!/usr/bin/env python3
"""
Focused test to find exact failure point between 30,000 and 35,000 characters.
"""

import os
import tempfile
import shutil
from llama_index.core import Settings, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama

# LLM Configuration
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


def load_actual_document():
    """Load the actual document to see its real size."""
    try:
        pdf_path = "/Users/imjoseangel/Downloads/PDF/The_Imitation_Game.pdf"
        temp_dir = tempfile.mkdtemp()
        filename = os.path.basename(pdf_path)
        dest_path = os.path.join(temp_dir, filename)
        shutil.copy2(pdf_path, dest_path)

        documents = SimpleDirectoryReader(temp_dir).load_data()

        if documents:
            doc_text = documents[0].text.strip()
        else:
            doc_text = ""

        shutil.rmtree(temp_dir, ignore_errors=True)
        return doc_text
    except Exception as e:
        print(f"Error loading document: {e}")
        return ""


def create_extended_content(base_content, target_size):
    """Create extended content by repeating the base content."""
    if len(base_content) >= target_size:
        return base_content[:target_size]

    # Repeat the content until we reach target size
    repetitions = (target_size // len(base_content)) + 1
    extended = (base_content + "\n\n") * repetitions
    return extended[:target_size]


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


def run_focused_test():
    """Run focused tests between 30,000 and 35,000 to find exact limit."""

    # Load the actual document
    base_content = load_actual_document()

    if not base_content:
        print("Failed to load base document")
        return

    print(f"Base document size: {len(base_content)} characters")
    print("Finding exact failure point...\n")

    # Test sizes between 30,000 and 35,000
    sizes = [30000, 31000, 32000, 33000, 34000, 34500, 35000]

    print(f"{'Size':<6} {'Content':<8} {'Message':<8} {'Status':<8} {'Response Preview'}")
    print("-" * 90)

    for size in sizes:
        print(f"{size:<6}", end=" ")

        # Create extended content
        extended_content = create_extended_content(base_content, size)

        # Test with LLM
        result = test_llm_with_content(extended_content)

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

    print("\n" + "="*80)
    print("SUMMARY:")
    print(f"- Context window: 8096 tokens")
    print(f"- Estimated tokens ≈ message_length / 4")
    print(f"- 30,000 chars ≈ 7,500 tokens (within limit)")
    print(f"- 35,000 chars ≈ 8,750 tokens (exceeds limit)")
    print(f"- Safe limit appears to be around 32,000 characters")


if __name__ == "__main__":
    run_focused_test()
