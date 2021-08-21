#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    arr = []

    for _ in range(6):
        arr.append(list(map(int, input().rstrip().split())))

    items = [[arr[i][j:j + 3], arr[i + 1][j + 1:j + 2], arr[i + 2][j:j + 3]]
             for j in range(len(arr[0]) - 2) for i in range(len(arr) - 2)]

    maxsum = 0

    for order in range(len(items)):
        total = 0

        for item in items[order]:
            total += sum(item)

        if total > maxsum:
            maxsum = total

    print(maxsum)


if __name__ == '__main__':
    main()
