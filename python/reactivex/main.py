#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Callable, cast
import reactivex as rx
from reactivex import operators as ops

source = rx.of("Alpha", "Beta", "Gamma", "Delta", "Epsilon")

composed = source.pipe(
    ops.map(len),
    ops.filter(cast(Callable[[int], bool], lambda i: i >= 5))
)

composed.subscribe(lambda value: print(f"Received {value}"))
