#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import sys
import re
import random
import os
import math


def main():

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])
    m = int(first_multiple_input[1])

    matrix = []
    startint = 0
    midstr = ""

    for _ in range(n):
        matrix_item = input()
        matrix.append(matrix_item)

    for x in range(m):
        for y in range(n):
            midstr += str(matrix[y][x])

    print(re.sub(r'\b[^a-zA-Z0-9]+\b', ' ', midstr))


if __name__ == '__main__':
    main()
