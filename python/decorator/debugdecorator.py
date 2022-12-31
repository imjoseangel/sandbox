#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rich import print as rprint
import functools


def uppercase_decorator(func):
    @functools.wraps(func)
    def wrapper():
        return func().upper()
    return wrapper


@uppercase_decorator
def say_hi():
    "This will say hi"
    return 'hello there'


rprint(say_hi())
rprint(say_hi.__name__)
rprint(say_hi.__doc__)
