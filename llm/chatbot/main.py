from llama_index.core import Settings
from llama_index.llms.gemini import Gemini

MODEL = "models/gemini-1.5-flash-latest"

Settings.llm = Gemini(
    model=MODEL,
    request_timeout=120.0,
    temperature=0.0,
)
