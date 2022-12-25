#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rich import print as rprint


def plus_one(number):
    return number + 1


def function_call(function):
    number_to_add = 5
    return function(number_to_add)


rprint(function_call(plus_one))
