#!/usr/bin/env python3

import os
import tempfile
import shutil
from llama_index.core import SimpleDirectoryReader


def test_pdf_loading(pdf_path):
    """Test loading a PDF document."""
    try:
        # Create a temporary directory for the uploaded files
        temp_dir = tempfile.mkdtemp()

        # Copy PDF to temp directory
        if os.path.exists(pdf_path):
            filename = os.path.basename(pdf_path)
            dest_path = os.path.join(temp_dir, filename)
            shutil.copy2(pdf_path, dest_path)
            print(f"Copied file {pdf_path} to {dest_path}")

        # Load documents using SimpleDirectoryReader
        documents = SimpleDirectoryReader(temp_dir).load_data()
        print(f"Loaded {len(documents)} documents")

        # Extract text content from all documents
        for i, doc in enumerate(documents):
            file_name = doc.metadata.get('file_name', 'Unknown')
            print(f"\n=== DOCUMENT {i+1}: {file_name} ===")
            print(f"Content length: {len(doc.text)} characters")
            print(f"First 500 characters:")
            print(doc.text[:500])
            print("...")
            print(f"Last 500 characters:")
            print(doc.text[-500:])

        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

    except Exception as e:
        print(f"Error loading documents: {e}")


if __name__ == "__main__":
    pdf_path = "/Users/imjoseangel/Downloads/PDF/The_Imitation_Game.pdf"
    test_pdf_loading(pdf_path)
