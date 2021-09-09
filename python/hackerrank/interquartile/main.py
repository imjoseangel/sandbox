#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import statistics


def interQuartile(values, freqs):

    s = []

    for item in range(len(values)):
        s += [values[item]] * freqs[item]

    N = sum(freqs)
    s.sort()

    if N % 2 != 0:
        q1 = statistics.median(s[:N // 2])
        q3 = statistics.median(s[N // 2 + 1:])
    else:
        q1 = statistics.median(s[:N // 2])
        q3 = statistics.median(s[N // 2:])

    ir = round(float(q3 - q1), 1)
    return ir


def main():
    n = int(input().strip())
    val = list(map(int, input().rstrip().split()))
    freq = list(map(int, input().rstrip().split()))

    print(interQuartile(val, freq))


if __name__ == '__main__':
    main()
