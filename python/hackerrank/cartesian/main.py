#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from itertools import product


def main():

    A = (map(int, input().rstrip().split()))
    B = (map(int, input().rstrip().split()))

    result = product(A, B)
    print(*result)


if __name__ == '__main__':
    main()
