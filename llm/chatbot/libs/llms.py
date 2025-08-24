import logging
import os
import sys
import urllib3

from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

logger = logging.getLogger(__name__)

# LLM Configuration
OLLAMA_MODEL = "qwen3:8b"
OPENAI_MODEL = "openai/gpt-oss-20b:free"
OLLAMA_EMBED_MODEL = "nomic-embed-text:v1.5"
OPENAI_EMBED_MODEL = "text-embedding-nomic-embed-text-v1.5"

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OPENAI_HOST = os.getenv("OPENAI_HOST", "http://127.0.0.1:1234/v1")


def test_conn(conn_type):
    host_url = globals()[f"{conn_type.upper()}_HOST"]

    try:
        timeout = urllib3.Timeout(connect=2.0, read=7.0)
        http = urllib3.PoolManager(timeout=timeout)
        response = http.request("GET", host_url)

        logger.debug(
            f"Testing connection to {conn_type.capitalize()} API at {host_url}")

        if response.status == 200:
            logger.info(
                f"Connected to {conn_type.capitalize()} API successfully.")
        else:
            logger.error(
                f"Failed to connect to {conn_type.capitalize()} API: {response.status}")
    except urllib3.exceptions.HTTPError as e:
        logger.error(f"Error connecting to {conn_type.capitalize()} API: {e}")
        sys.exit(1)


def Ollama_Setup():

    test_conn("OLLAMA")

    Settings.llm = Ollama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_HOST,
        thinking=False,
        temperature=0.0,
        max_retries=5,
        context_window=8096,
    )

    Settings.embed_model = OllamaEmbedding(
        model_name=OLLAMA_EMBED_MODEL,
        base_url=OLLAMA_HOST,
    )


def OpenAI_Setup():

    test_conn("OPENAI")

    Settings.llm = OpenAI(
        model_name=OPENAI_MODEL,
        api_base=OPENAI_HOST,
        thinking=False,
        temperature=0.0,
        max_retries=5,
        context_window=8096,
    )

    Settings.embed_model = OpenAIEmbedding(
        model_name=OPENAI_EMBED_MODEL,
        api_base=OPENAI_HOST,
    )
