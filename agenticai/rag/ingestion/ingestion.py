import os
import sys
import loguru
import pymongo
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    Settings,
    VectorStoreIndex,
)

from llama_index.core.extractors import (TitleExtractor,
                                         QuestionsAnsweredExtractor,
                                         KeywordExtractor,
                                         SummaryExtractor)
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.readers.file import PyMuPDFReader

from pymongo.operations import SearchIndexModel

# --- Configuration ---
MONGO_PASSWORD = os.getenv("MONGODB_PASSWORD")
if not MONGO_PASSWORD:
    loguru.logger.error(
        "Error: MONGODB_PASSWORD environment variable not set.")
    sys.exit(1)


MONGO_DB = "XX"
MONGO_HOST = "xx.mongodb.net"
MONGO_CONNECTION_STRING = f"mongodb+srv://{MONGO_DB}:{MONGO_PASSWORD}@{MONGO_HOST}/"
MONGO_COLLECTION = "testpdf"
MONGO_VECTORINDEX = "test_index"


MODEL = "gemma3:latest"
EMBEDDING = "nomic-embed-text:latest"


Settings.llm = Ollama(model=MODEL,
                      request_timeout=300.0,
                      temperature=0.0,
                      context_window=2048
                      )


Settings.embed_model = OllamaEmbedding(
    model_name=EMBEDDING,
    ollama_additional_kwargs={"mirostat": 0, },
    timeout=300.0
)
Settings.chunk_size = 100
Settings.chunk_overlap = 10

# --- Data Loading ---
sample_data = SimpleDirectoryReader(
    input_dir="./docs",
    file_extractor={".pdf": PyMuPDFReader()}
).load_data()


loguru.logger.info(sample_data[0])

# --- Metadata Extraction Pipeline ---
text_splitter = TokenTextSplitter(
    separator=" ",
    chunk_size=512,
    chunk_overlap=128
)

title_extractor = TitleExtractor(nodes=5)
qa_extractor = QuestionsAnsweredExtractor(questions=3)
keyword_extractor = KeywordExtractor(keywords=15)
summary_extractor = SummaryExtractor(
    summaries=["prev", "self"], nodes=5, num_workers=5)


pipeline = IngestionPipeline(
    transformations=[text_splitter, title_extractor,
                     qa_extractor,
                     keyword_extractor,
                     summary_extractor
                     ]
)

# Process documents to extract nodes with metadata
nodes = pipeline.run(
    documents=sample_data,
    in_place=True,
    show_progress=True,
)

# --- MongoDB Connection ---
mongo_client: pymongo.MongoClient = pymongo.MongoClient(
    MONGO_CONNECTION_STRING)

# --- Vector Store Setup ---
atlas_vector_store = MongoDBAtlasVectorSearch(
    mongo_client,
    db_name=MONGO_DB,
    collection_name=MONGO_COLLECTION,
    vector_index_name=MONGO_VECTORINDEX
)
vector_store_context = StorageContext.from_defaults(
    vector_store=atlas_vector_store)

vector_store_index = VectorStoreIndex(
    nodes, storage_context=vector_store_context, show_progress=True
)

# --- MongoDB Atlas Search Index Setup ---
collection = mongo_client[MONGO_DB][MONGO_COLLECTION]
search_index_model = SearchIndexModel(
    definition={
        "fields": [
            {
                "type": "vector",
                "path": "embedding",
                "numDimensions": 768,
                "similarity": "cosine"
            },
            {
                "type": "filter",
                "path": "metadata.document_title"
            },
            {
                "type": "filter",
                "path": "metadata.excerpt_keywords"
            },
            {
                "type": "filter",
                "path": "metadata.section_summary"
            },
            {
                "type": "filter",
                "path": "metadata.questions_this_excerpt_can_answer"
            },
        ]
    },
    name=MONGO_VECTORINDEX,
    type="vectorSearch"
)

try:
    collection.create_search_index(model=search_index_model)
    loguru.logger.info(f"Created search index {MONGO_VECTORINDEX}")
except Exception as e:
    loguru.logger.warning(f"Could not create search index: {e}")

loguru.logger.info(
    "Ingestion, metadata extraction, and indexing completed successfully.")

# pip install pymupdf pdfminer.six
