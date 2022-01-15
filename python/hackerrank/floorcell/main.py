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
    A = numpy.array(list(map(float, input().split())))
    numpy.set_printoptions(legacy='1.13')
    print(numpy.floor(A), numpy.ceil(A), numpy.rint(A), sep='\n')


if __name__ == '__main__':
    main()
