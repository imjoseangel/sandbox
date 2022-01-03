#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import numpy


def arrays(arr):
    # complete this function
    # use numpy.array
    a = numpy.array(arr, float)
    return a[::-1]


def main():
    """
    Main function
    """
    arr = input().strip().split(' ')
    result = arrays(arr)
    print(result)


if __name__ == '__main__':
    main()
