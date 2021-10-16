#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    X = list(map(int, input().rstrip().split()))
    A = []

    for _ in range(X[1]):
        A.append(input().rstrip().split())

    print(list(zip(*A)))


if __name__ == '__main__':
    main()
