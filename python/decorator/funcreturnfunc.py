#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rich import print as rprint


def hello_function():
    def say_hi():
        return "Hi"
    return say_hi


hello = hello_function()
rprint(hello())
