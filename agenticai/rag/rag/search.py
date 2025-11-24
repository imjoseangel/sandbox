import os
import sys

import pymongo
import loguru

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.settings import Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.question_gen import LLMQuestionGenerator
from llama_index.core.question_gen.prompts import (
    DEFAULT_SUB_QUESTION_PROMPT_TMPL,
)

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
                      request_timeout=120.0,
                      temperature=0.0,
                      context_window=2048,
                      )


Settings.embed_model = OllamaEmbedding(
    model_name=EMBEDDING,
    ollama_additional_kwargs={"mirostat": 0, },
    request_timeout=120.0
)
Settings.chunk_size = 100
Settings.chunk_overlap = 10

# Connect to your Atlas cluster
mongo_client: pymongo.MongoClient = pymongo.MongoClient(
    MONGO_CONNECTION_STRING)

# Instantiate the vector store
atlas_vector_store = MongoDBAtlasVectorSearch(
    mongo_client,
    db_name=MONGO_DB,
    collection_name=MONGO_COLLECTION,
    vector_index_name=MONGO_VECTORINDEX,
)

vector_store_context = StorageContext.from_defaults(
    vector_store=atlas_vector_store)

vector_store_index = VectorStoreIndex.from_vector_store(
    vector_store=atlas_vector_store,
    storage_context=vector_store_context,
)

question_gen = LLMQuestionGenerator.from_defaults(
    prompt_template_str="""
        Follow the example, but instead of giving a question, always prefix the question
        with: 'By first identifying and quoting the most relevant sources, '.
        """
    + DEFAULT_SUB_QUESTION_PROMPT_TMPL,
)

engine = vector_store_index.as_query_engine(
    similarity_top_k=10)


final_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=[
        QueryEngineTool(
            query_engine=engine,
            metadata=ToolMetadata(
                name="anatomy_documents",
                description="Anatomy documents for answering questions about anatomy and related topics.",
            ),
        )
    ],
    question_gen=question_gen,
    use_async=True,
)

response = final_engine.query(
    """
    What is a somatosensory system?
    """
)
print(response)
