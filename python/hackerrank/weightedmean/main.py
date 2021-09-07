#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def weightedMean(X, W):

    return round(sum([i[0] * i[1] for i in zip(X, W)]) / sum(W), 1)


def main():
    n = int(input().strip())

    vals = list(map(int, input().rstrip().split()))

    weights = list(map(int, input().rstrip().split()))

    print(weightedMean(vals, weights))


if __name__ == '__main__':
    main()
