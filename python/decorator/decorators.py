#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rich import print as rprint


def uppercase_decorator(function):
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase

    return wrapper


def say_hi():
    return "hello there"


decorate = uppercase_decorator(say_hi)
rprint(decorate())


@uppercase_decorator
def say_lo():
    return "what's up"


print(say_lo())
