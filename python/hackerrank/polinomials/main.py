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

    N = list(map(float, input().split()))
    x = int(input())

    print(numpy.polyval(N, x))


if __name__ == '__main__':
    main()
