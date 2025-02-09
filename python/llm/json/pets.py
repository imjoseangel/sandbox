from ollama import chat
from pydantic import BaseModel


class Pet(BaseModel):
    name: str
    animal: str
    age: int
    color: str | None
    favorite_toy: str | None


class PetList(BaseModel):
    pets: list[Pet]


response = chat(
    messages=[
        {
            'role': 'user',
            'content': '''
        I have two pets.
        A cat named Luna who is 5 years old and loves playing with yarn. She has grey fur.
        I also have a 2 year old black cat named Loki who loves tennis balls.
      ''',
        }
    ],
    model='gemma2:9b',
    format=PetList.model_json_schema(),
)

if response.message.content is None:
    raise ValueError("No response from LLM")
else:
    pets = PetList.model_validate_json(response.message.content)
    print(pets)
