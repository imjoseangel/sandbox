#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import math
import os
import random
import re
import sys


def isWinning(n, config):

    # precompute the Sprague-Grundy (SG) function for all 0 <= n <= 300
    g = [0, 1, 2]
    for n in range(3, 301):
        s = set()
        # hit one or two pins
        for l in (1, 2):
            # the group of n pins can be split into two
            # grops of i and n - l - i pins
            for i in range(int((n - l) / 2 + 1)):
                s.add(g[i] ^ g[n - l - i])
        # compute mex (minimum excluded value)
        m = 0
        while m in s:
            m += 1
        g.append(m)

    ret = 0
    # split the pins into groups and xor the SG values
    for p in config.strip().split('X'):
        ret ^= g[len(p)]
    return 'WIN' if ret else 'LOSE'


def main():
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t = int(input().strip())

    for t_itr in range(t):
        n = int(input().strip())

        config = input()

        result = isWinning(n, config)

        fptr.write(result + '\n')

    fptr.close()


if __name__ == '__main__':
    main()
