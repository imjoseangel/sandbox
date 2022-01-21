#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def divisibleSumPairs(_, k, ar):
    # Write your code here
    count = 0
    for _, i in enumerate(ar):
        for j in ar[_ + 1:]:
            if (i + j) % k == 0:
                count += 1
    return count


def main():
    """
    Main function
    """
    first_multiple_input = input().rstrip().split()
    n = int(first_multiple_input[0])
    k = int(first_multiple_input[1])

    ar = list(map(int, input().rstrip().split()))

    result = divisibleSumPairs(n, k, ar)
    print(result)


if __name__ == '__main__':
    main()
