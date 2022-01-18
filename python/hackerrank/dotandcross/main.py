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

    N = int(input())

    A = numpy.array([input().split() for _ in range(N)], int)
    B = numpy.array([input().split() for _ in range(N)], int)

    print(numpy.dot(A, B))


if __name__ == '__main__':
    main()
