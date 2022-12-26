#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rich import print as rprint


def uppercase_decorator(function):
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase

    return wrapper


def split_string(function):
    def wrapper():
        func = function()
        splitted_string = func.split()
        return splitted_string

    return wrapper


def say_hi():
    return "hello there"


decorate = uppercase_decorator(say_hi)
rprint(decorate())


@split_string
@uppercase_decorator
def say_lo():
    return "what's up"


print(say_lo())
