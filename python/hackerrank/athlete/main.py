#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    nm = input().split()

    n = int(nm[0])
    m = int(nm[1])

    arr = []

    for _ in range(n):
        arr.append(list(map(int, input().rstrip().split())))

    k = int(input())

    sorted_arr = sorted(arr, key=lambda x: x[k])

    for item in sorted_arr:
        print(item)


if __name__ == '__main__':
    main()
