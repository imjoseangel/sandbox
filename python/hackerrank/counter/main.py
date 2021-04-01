#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from collections import Counter


def main():
    X = int(input())
    S = list(map(int, input().rstrip().split()))
    N = int(input())

    print(N, S)


if __name__ == '__main__':
    main()
