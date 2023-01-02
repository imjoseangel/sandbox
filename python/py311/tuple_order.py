# tuple_order.py
from typing import TypeVar, TypeVarTuple

T0 = TypeVar("T0")
Ts = TypeVarTuple("Ts")


def cycle(elements: tuple[T0, *Ts]) -> tuple[*Ts, T0]:
    first, *rest = elements
    return (*rest, first)
