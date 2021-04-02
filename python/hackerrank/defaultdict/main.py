#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from collections import defaultdict


def main():
    A, B = (list(map(int, input().split())))

    X = defaultdict(list)
    Z = defaultdict(list)

    for _ in range(A):
        item = input().split()
        X['A'].append(item[0])

    for _ in range(B):
        item = input().split()
        Z['B'].append(item[0])

    for item in Z.get('B'):
        if item not in X.get('A'):
            print(-1)
        else:
            Y = [index + 1 for index,
                 element in enumerate(X.get('A')) if element == item]

            for item in Y:
                print(item, end=' ')
            print('')


if __name__ == '__main__':
    main()
