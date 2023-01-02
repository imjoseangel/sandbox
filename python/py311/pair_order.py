# pair_order.py
from typing import TypeVar

T0 = TypeVar("T0")
T1 = TypeVar("T1")


def flip(pair: tuple[T0, T1]) -> tuple[T1, T0]:
    first, second = pair
    return (second, first)
