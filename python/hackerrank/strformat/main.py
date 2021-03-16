#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def print_formatted(n):

    size = len(f"{n:b}")

    for dec in range(1, n + 1):
        print(
            f"{dec: >{size}} {dec: >{size}o} {dec: >{size}X} {dec: >{size}b}")


if __name__ == '__main__':
    n = 17
    print_formatted(n)
