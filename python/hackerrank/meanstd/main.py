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

    N, _ = map(int, input().split())
    my_array = numpy.array([input().split() for _ in range(N)], int)

    print(numpy.mean(my_array, axis=1))
    print(numpy.var(my_array, axis=0))
    numpy.set_printoptions(legacy='1.13')
    print(round(numpy.std(my_array), 11))


if __name__ == '__main__':
    main()
