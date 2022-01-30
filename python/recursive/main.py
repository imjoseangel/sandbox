#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def func(x, ans):
    """
    Function to calculate the value of the function
    """
    try:
        if x == 0:
            return 0
        return func(x - 1, x + ans)
    except RecursionError:
        return -1


def main():
    """
    Main function
    """
    print(func(-2, 66))


if __name__ == '__main__':
    main()
