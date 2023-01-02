from typing import Sequence, TypeVar

T = TypeVar("T")


def first(sequence: Sequence[T]) -> T:
    return sequence[0]


print(first([1, 2, 3]))
