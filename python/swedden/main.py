#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sweddish Code
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def fun(n):
    if n == 0:
        return 2
    elif n == 1:
        return 1
    else:
        return fun(n - 1) + fun(n - 2)


def main():
    """
    Main function
    """

    s = ''

    for i in range(1, 6):
        s += str(fun(i))

    print(f'www.multisoft.se/{s}')


if __name__ == '__main__':
    main()
