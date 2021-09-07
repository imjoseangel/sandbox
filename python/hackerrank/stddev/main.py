#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def stdDev(arr):
    mean = sum(arr) / len(arr)
    diffs = [x - mean for x in arr]
    sqdiffs = [d ** 2 for d in diffs]
    sdev = (sum(sqdiffs) / len(arr)) ** 0.5
    return sdev


def main():
    n = int(input().strip())

    vals = list(map(int, input().rstrip().split()))

    print(stdDev(vals))


if __name__ == '__main__':
    main()
