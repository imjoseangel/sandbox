#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import numpy


def main():
    """
    Main function
    """
    n, m = map(int, input().split())
    n, m = map(int, input().split())

    a, b = (numpy.array([input().split() for _ in range(n)], dtype=int)
            for _ in range(2))

    print(a + b, a - b, a * b, a // b, a % b, a ** b, sep='\n')


if __name__ == '__main__':
    main()
