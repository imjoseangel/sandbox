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
    N, M = map(int, input().split())

    a = numpy.array(list(map(int, input().rstrip().split())), float)
    b = numpy.array(list(map(int, input().rstrip().split())), float)

    print(numpy.add(a, b))


if __name__ == '__main__':
    main()
