import logging
from typing import List, Optional

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, SummaryIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import FunctionTool
from llama_index.core.tools.tool_spec.base import BaseToolSpec

# --- Start Logging Configuration ---
logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class PDFTool(BaseToolSpec):
    """PDFTool for multi-PDF document operations with vector search."""

    def __init__(self, file_paths: Optional[List[str]] = None):
        self.file_paths = file_paths or []
        self.documents: List = []
        self.vector_index = None
        self.summary_index = None

        if self.file_paths:
            self._load_documents()

    def _load_documents(self):
        """Load all PDF documents and create indexes."""
        self.documents = SimpleDirectoryReader(
            input_files=self.file_paths).load_data()

        splitter = SentenceSplitter(chunk_size=512, chunk_overlap=64)
        nodes = splitter.get_nodes_from_documents(documents=self.documents)

        # Create vector index for all documents
        self.vector_index = VectorStoreIndex(nodes=nodes)

        # Create summary index from first 5 nodes of each document
        summary_nodes = []
        for doc in self.documents[:3]:  # First 3 documents
            doc_nodes = splitter.get_nodes_from_documents([doc])
            summary_nodes.extend(doc_nodes[:2])  # First 2 nodes per doc

        self.summary_index = SummaryIndex(summary_nodes)

    def update_documents(self, file_paths: List[str]):
        """Update the tool with new document paths."""
        self.file_paths = file_paths
        if file_paths:
            self._load_documents()

    spec_functions = ["search_documents", "summarize_documents"]

    def search_documents(self, query: str) -> str:
        """Search across all uploaded PDF documents for specific information.

        Args:
            query: The question or topic to search for in the documents

        Returns:
            Relevant information from the documents
        """
        logger.info(f"🔍 search_documents called with query: '{query}'")
        logger.info(
            f"📊 PDF tool state: docs={len(self.documents)}, vector_index={self.vector_index is not None}")

        if not self.vector_index:
            result = "No documents are currently loaded. Please upload PDF files first."
            logger.info(f"❌ No vector index available, returning: {result}")
            return result

        query_engine = self.vector_index.as_query_engine(similarity_top_k=5)
        response = query_engine.query(query)
        result = str(response)
        logger.info(f"✅ Search completed, result length: {len(result)}")
        return result

    def summarize_documents(self) -> str:
        """Generate a summary of all uploaded PDF documents.

        Returns:
            A comprehensive summary of the uploaded documents
        """
        logger.info("📋 summarize_documents called")
        logger.info(
            f"📊 PDF tool state: docs={len(self.documents)}, "
            f"summary_index={self.summary_index is not None}")

        if not self.summary_index:
            result = "No documents are currently loaded. Please upload PDF files first."
            logger.info(f"❌ No summary index available, returning: {result}")
            return result

        query_engine = self.summary_index.as_query_engine(
            response_mode="tree_summarize"
        )
        response = query_engine.query(
            "Provide a comprehensive summary of these documents")
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
            fn=self.search_documents,
            name="search_documents",
            description=(
                "ALWAYS use this tool when the user asks questions about uploaded PDF documents, "
                "asks for information from documents, or wants to find specific content in PDFs. "
                "This tool searches across all uploaded PDF files using vector similarity."
            ),
            return_direct=True,
        )

        summary_tool = FunctionTool.from_defaults(
            fn=self.summarize_documents,
            name="summarize_documents",
            description=(
                "ALWAYS use this tool when the user asks for a summary, overview, or general "
                "information about uploaded PDF documents. This tool generates comprehensive "
                "summaries from all uploaded PDFs."
            ),
            return_direct=True,
        )

        return [search_tool, summary_tool]
