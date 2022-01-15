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

    print(numpy.floor(A))


if __name__ == '__main__':
    main()
