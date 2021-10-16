#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    X = list(map(int, input().rstrip().split()))
    A = []

    for _ in range(X[1]):
        A.append(input().rstrip().split())

    for item in (list(zip(*A))):
        print(sum(list(map(float, item))) / len(item))


if __name__ == '__main__':
    main()
