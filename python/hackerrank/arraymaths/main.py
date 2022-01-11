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

    a = numpy.array(list(map(int, input().rstrip().split())))
    b = numpy.array(list(map(int, input().rstrip().split())))

    print(a + b, a - b, a * b, a // b, a % b, a ** b, sep='\n')


if __name__ == '__main__':
    main()
