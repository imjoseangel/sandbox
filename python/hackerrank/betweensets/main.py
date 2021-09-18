#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def getTotalX(a, b):
    validCount = 0

    for number in range(max(a), min(b) + 1):
        left = all(number % index == 0 for index in a)
        right = all(index % number == 0 for index in b)

        validCount += left and right

    return validCount


def main():
    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    m = int(first_multiple_input[1])

    arr = list(map(int, input().rstrip().split()))
    brr = list(map(int, input().rstrip().split()))

    total = getTotalX(arr, brr)

    print(str(total), end="\n")


if __name__ == '__main__':
    main()
