#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rich import print as rprint


def plus_one(number):
    def add_one(number):
        return number + 1

    result = add_one(number)
    return result


rprint(plus_one(4))
