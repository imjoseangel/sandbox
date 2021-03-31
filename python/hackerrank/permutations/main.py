#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from itertools import permutations
import string


def main():
    n, m = input().split()
    result = list(permutations(n, int(m)))

    sortedresult = sorted(result, key=lambda tup: (tup[0], tup[1]))

    for item in sortedresult:
        print(f"{item[0]}{item[1]}")


if __name__ == '__main__':
    main()
