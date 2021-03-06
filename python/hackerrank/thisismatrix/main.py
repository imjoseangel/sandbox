#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import re


def main():

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])
    m = int(first_multiple_input[1])

    matrix = []

    for _ in range(n):
        matrix_item = input()
        matrix.append(matrix_item)

    midstr = ""

    for x in range(m):
        for y in range(n):
            midstr += str(matrix[y][x])

    print(re.sub(r'\b[^a-zA-Z0-9]+\b', ' ', midstr))


if __name__ == '__main__':
    main()
