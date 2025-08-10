from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, SummaryIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import QueryEngineTool
from llama_index.core.tools.tool_spec.base import BaseToolSpec


class PDFTool(BaseToolSpec):
    """PDFTool is a base class for PDF document operations.
    It provides methods to extract text and metadata from PDF files.
    """

    def __init__(self, file_path: str):
        self.document = SimpleDirectoryReader(
            input_files=[file_path]).load_data()
        self.name = self.document[0].metadata['file_name'].split('.')[0]
        self.splitter = SentenceSplitter(chunk_size=512, chunk_overlap=64)
        self.nodes = self.splitter.get_nodes_from_documents(
            documents=self.document)

        self.vector_index = VectorStoreIndex(nodes=self.nodes)
        self.vector_query_engine = self.vector_index.as_query_engine(
            similarity_top_k=5)
        self.summary_index = SummaryIndex(self.nodes[:3])
        self.summary_query_engine = self.summary_index.as_query_engine(
            response_mode="tree_summarize"
        )

    spec_functions = ["query", "summary"]

    def query(self) -> QueryEngineTool:
        """
        Extract text content from a PDF file.
        Returns a query engine tool for extracting text from the loaded document.
        """
        vector_query_tool = QueryEngineTool.from_defaults(
            name=f"vector_tool_{self.name}",
            query_engine=self.vector_query_engine,
            description=(
                "Useful for specific topic based questions"
                "Do NOT use if you need a summary of the document."
            )
        )

        return vector_query_tool

    def summary(self) -> QueryEngineTool:
        """
        Generate a summary of the PDF document.
        Returns a summary of the loaded document.
        """

        summary_tool = QueryEngineTool.from_defaults(
            name=f"summary_tool_{self.name}",
            query_engine=self.summary_query_engine,
            description=(
                "Use ONLY IF you want to get a summary of the document. "
                "Do NOT use if you have specific questions related to document."
            )
        )

        return summary_tool
