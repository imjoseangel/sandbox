#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from itertools import combinations


def main():
    n, m = input().split()

    for item in range(1, int(m) + 1):
        print(*[''.join(i)
              for i in combinations(sorted(n), int(item))], sep='\n')


if __name__ == '__main__':
    main()
