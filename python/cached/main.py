#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from timeit import timeit

loop_squared = 6_000


def cached():
    """
    Instead of referencing the module every time to find the
    method we're after, we cache it into a local variable
    to use within the loop
    """

    now = datetime.datetime.now  # Cache the method call
    for _ in range(loop_squared):
        now()


def not_cached():
    """
    Referencing the module every loop will be slower
    and less efficient
    """

    for _ in range(loop_squared):
        datetime.datetime.now()


print(
    timeit(cached, number=loop_squared)
)  # = > 10.985265999999683

print(
    timeit(not_cached, number=loop_squared)
)  # => 12.54908033400352
