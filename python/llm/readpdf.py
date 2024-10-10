from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

documents = SimpleDirectoryReader(
    "/Users/imjoseangel/Downloads/PDF").load_data()

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-base-en-v1.5", cache_folder="./cache")

Settings.llm = Ollama(model="gemma2:latest",
                      temperature=0, request_timeout=120.0)

index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query(
    "¿Puedes resumir las condiciones generales en Español?", verbose=True)
print(response)
