#!/usr/bin/env python3
"""
Test the simplified single document PDF tool
"""
from main import pdf_tool, SUPPORTED_TOOLS, GradioReActAgentPack
import tempfile
import os

def test_single_document():
    """Test single document upload and processing"""
    print("🧪 Testing Simplified Single Document PDF Tool")
    
    # Create a simple PDF for testing
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        # Create a minimal PDF with some content
        pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 50 >>
stream
BT
/F1 12 Tf
100 700 Td
(This is a test document about AI and technology.) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000010 00000 n
0000000053 00000 n
0000000125 00000 n
0000000229 00000 n
trailer
<< /Size 5 /Root 1 0 R >>
startxref
329
%%EOF"""
        tmp.write(pdf_content)
        test_pdf_path = tmp.name

    try:
        print(f"📄 Created test PDF: {test_pdf_path}")
        
        # Test 1: Initial state
        print("\n1️⃣ Testing initial state:")
        print(f"   Document loaded: {pdf_tool.document is not None}")
        print(f"   Vector index: {pdf_tool.vector_index is not None}")
        
        # Test 2: Load document
        print("\n2️⃣ Loading document:")
        pdf_tool.update_document(test_pdf_path)
        print(f"   Document loaded: {pdf_tool.document is not None}")
        print(f"   Vector index: {pdf_tool.vector_index is not None}")
        print(f"   Summary index: {pdf_tool.summary_index is not None}")
        
        # Test 3: Search functionality
        print("\n3️⃣ Testing search:")
        search_result = pdf_tool.search_document("What is this document about?")
        print(f"   Search result: {search_result[:100]}...")
        
        # Test 4: Summary functionality
        print("\n4️⃣ Testing summary:")
        summary_result = pdf_tool.summarize_document()
        print(f"   Summary result: {summary_result[:100]}...")
        
        # Test 5: Clear document
        print("\n5️⃣ Testing clear:")
        pdf_tool.update_document("")
        print(f"   Document cleared: {pdf_tool.document is None}")
        print(f"   Vector index cleared: {pdf_tool.vector_index is None}")
        
        # Test 6: Agent integration
        print("\n6️⃣ Testing agent integration:")
        agent_pack = GradioReActAgentPack(supported_tools=SUPPORTED_TOOLS)
        success = agent_pack._load_documents_from_files([test_pdf_path])
        print(f"   Agent load success: {success}")
        print(f"   Agent PDF tool state: document={agent_pack.pdf_tool.document is not None}")
        
        print("\n🎉 All tests completed successfully!")
        
    finally:
        # Cleanup
        try:
            os.unlink(test_pdf_path)
        except:
            pass

if __name__ == "__main__":
    test_single_document()
