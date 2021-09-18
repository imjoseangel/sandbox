#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from itertools import combinations


def main():
    _ = int(input())

    l = list(input().split())
    k = int(input())

    aonly = len([item for item in list(combinations(l, k)) if 'a' in item])
    allcomb = len(list(combinations(l, k)))

    print(f"{aonly / allcomb:.12f}")


if __name__ == '__main__':
    main()
