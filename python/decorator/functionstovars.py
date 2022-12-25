#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rich import print as rprint


def plus_one(number):
    return number + 1


add_one = plus_one
rprint(add_one(5))
