#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    n = int(input().strip())
    a = list(map(int, input().rstrip().split()))

    swap = []
    for i in range(n):
        numberOfSwaps = 0

        for j in range(n - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]

                swap.append(a[i])
                numberOfSwaps += 1

        if numberOfSwaps == 0:
            break

    print(f'Array is sorted in {len(swap)} swaps.')
    print('First Element:', a[0])
    print('Last Element:', a[-1])


if __name__ == '__main__':
    main()
