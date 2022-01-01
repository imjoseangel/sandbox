#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def wrapper(f):
    def fun(l):
        # complete the function
        f(["+91 " + item[-10:-5] + " " + item[-5:] for item in l])

    return fun


@wrapper
def sort_phone(l):
    print(*sorted(l), sep='\n')


def main():
    l = [input() for _ in range(int(input()))]
    sort_phone(l)


if __name__ == '__main__':
    main()
