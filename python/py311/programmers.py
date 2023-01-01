# programmers.py
from dataclasses import dataclass
import json
import pathlib
from rich import print as rprint

programmers = json.loads(pathlib.Path(
    "programmers.json").read_text(encoding="utf-8"))


@dataclass
class Person:
    name: str
    life_span: tuple[int, int]

    @classmethod
    def from_dict(cls, info):
        return cls(
            name=f"{info['name']['first']} {info['name']['last']}",
            life_span=(info["birth"]["year"], info["death"]["year"]),
        )


def convert_pair(first, second):
    return Person.from_dict(first), Person.from_dict(second)
