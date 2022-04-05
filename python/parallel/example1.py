#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import ray


@ray.remote
def func1(x):
    return x + 1


@ray.remote
def func2(y):
    return y + 1


def main():
    """
    Main function
    """
    ray.init()
    funcs = []
    funcs.append(func1.remote(x=2))
    funcs.append(func2.remote(y=2))
    results = ray.get(funcs)
    print(results)


if __name__ == '__main__':
    main()
