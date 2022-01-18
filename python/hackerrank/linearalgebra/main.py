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

    A = numpy.array([input().split() for _ in range(N)], numpy.float64)

    print(numpy.linalg.det(A))


if __name__ == '__main__':
    main()
