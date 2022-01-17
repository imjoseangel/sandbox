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

    # print(numpy.max(numpy.min(my_array, axis=1)))


if __name__ == '__main__':
    main()
