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

    A = numpy.array(list(map(int, input().split())), int)
    B = numpy.array(list(map(int, input().split())), int)

    print(numpy.inner(A, B))
    print(numpy.outer(A, B))


if __name__ == '__main__':
    main()
