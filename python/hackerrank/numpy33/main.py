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
    my_array = numpy.array(list(map(int, input().strip().split(' '))))
    print(numpy.reshape(my_array, (3, 3)))


if __name__ == '__main__':
    main()
