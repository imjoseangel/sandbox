from typing import List, Optional
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, SummaryIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import FunctionTool
from llama_index.core.tools.tool_spec.base import BaseToolSpec


class PDFTool(BaseToolSpec):
    """PDFTool for single PDF document operations with vector search."""

    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path
        self.document = None
        self.vector_index = None
        self.summary_index = None
        
        if self.file_path:
            self._load_document()

    def _load_document(self):
        """Load the PDF document and create indexes."""
        if not self.file_path:
            return
            
        # Load single document
        documents = SimpleDirectoryReader(input_files=[self.file_path]).load_data()
        if not documents:
            return
            
        self.document = documents[0]
        
        # Create nodes from document
        splitter = SentenceSplitter(chunk_size=512, chunk_overlap=64)
        nodes = splitter.get_nodes_from_documents([self.document])
        
        # Create vector index for searching
        self.vector_index = VectorStoreIndex(nodes=nodes)
        
        # Create summary index from first few nodes
        summary_nodes = nodes[:5]  # Use first 5 nodes for summary
        self.summary_index = SummaryIndex(summary_nodes)

    def update_document(self, file_path: str):
        """Update the tool with a new document path."""
        self.file_path = file_path
        if file_path:
            self._load_document()
        else:
            # Clear everything if no file path
            self.file_path = None
            self.document = None
            self.vector_index = None
            self.summary_index = None

    spec_functions = ["search_document", "summarize_document"]

    def search_document(self, query: str) -> str:
        """Search the uploaded PDF document for specific information.
        
        Args:
            query: The question or topic to search for in the document
            
        Returns:
            Relevant information from the document
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"🔍 search_document called with query: '{query}'")
        logger.info(f"📊 PDF tool state: document={self.document is not None}, vector_index={self.vector_index is not None}")
        
        if not self.vector_index:
            result = "No document is currently loaded. Please upload a PDF file first."
            logger.info(f"❌ No vector index available, returning: {result}")
            return result

        query_engine = self.vector_index.as_query_engine(similarity_top_k=3)
        response = query_engine.query(query)
        result = str(response)
        logger.info(f"✅ Search completed, result length: {len(result)}")
        return result

    def summarize_document(self) -> str:
        """Generate a summary of the uploaded PDF document.
        
        Returns:
            A comprehensive summary of the uploaded document
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"📋 summarize_document called")
        logger.info(f"📊 PDF tool state: document={self.document is not None}, summary_index={self.summary_index is not None}")
        
        if not self.summary_index:
            result = "No document is currently loaded. Please upload a PDF file first."
            logger.info(f"❌ No summary index available, returning: {result}")
            return result

        query_engine = self.summary_index.as_query_engine(
            response_mode="tree_summarize"
        )
        response = query_engine.query(
            "Provide a comprehensive summary of this document")
        result = str(response)
        logger.info(f"✅ Summary completed, result length: {len(result)}")
        return result

    def to_tool_list(
        self,
        spec_functions=None,
        func_to_metadata_mapping=None,
    ) -> List[FunctionTool]:
        """Convert PDF functions to FunctionTool list."""
        search_tool = FunctionTool.from_defaults(
            fn=self.search_document,
            name="search_document",
            description=(
                "ALWAYS use this tool when the user asks questions about the uploaded PDF document, "
                "asks for information from the document, or wants to find specific content in the PDF. "
                "This tool searches the uploaded PDF file using vector similarity."
            ),
            return_direct=True,
        )
        
        summary_tool = FunctionTool.from_defaults(
            fn=self.summarize_document,
            name="summarize_document", 
            description=(
                "ALWAYS use this tool when the user asks for a summary, overview, or general "
                "information about the uploaded PDF document. This tool generates a comprehensive "
                "summary from the uploaded PDF."
            ),
            return_direct=True,
        )
        
        return [search_tool, summary_tool]
