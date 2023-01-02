# programmers.py
from dataclasses import dataclass
# This works with python >= 3.11
from typing import Any, Self
import json
import pathlib

programmers = json.loads(pathlib.Path(
    "programmers.json").read_text(encoding="utf-8"))


@dataclass
class Person:
    name: str
    life_span: tuple[int, int]

    @classmethod
    def from_dict(cls, info: dict[str, Any]) -> Self:
        return cls(
            name=f"{info['name']['first']} {info['name']['last']}",
            life_span=(info["birth"]["year"], info["death"]["year"]),
        )


def convert_pair(first, second):
    return Person.from_dict(first), Person.from_dict(second)
