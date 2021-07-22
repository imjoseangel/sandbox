#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from itertools import product


def main():
    k, m = map(int, input().split())

    n = (list(map(int, input().split()))[1:] for _ in range(k))

    print(max(map(lambda lb: sum(item**2 for item in lb) % m, product(*n))))


if __name__ == '__main__':
    main()
