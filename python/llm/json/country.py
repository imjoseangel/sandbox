from ollama import chat
from pydantic import BaseModel


class Country(BaseModel):
    name: str
    capital: str
    languages: list[str]


response = chat(
    messages=[
        {
            'role': 'user',
            'content': 'Tell me about Italy',
        }
    ],
    model='gemma2:9b',
    format=Country.model_json_schema(),
)

if response.message.content is None:
    raise ValueError("No response from LLM")
else:
    country = Country.model_validate_json(response.message.content)
    print(country)
