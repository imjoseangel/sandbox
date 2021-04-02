#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from collections import Counter


def main():
    X = int(input())
    N = Counter(map(int, input().split()))
    R = 0

    for _ in range(int(input())):
        shoe, price = map(int, input().split())

        if N[shoe]:
            N[shoe] -= 1
            R += price

    print(R)


if __name__ == '__main__':
    main()
