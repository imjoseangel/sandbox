#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

#
# Complete the 'birthday' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY s
#  2. INTEGER d
#  3. INTEGER m
#


def birthday(s, d, m):
    # Write your code here
    count = 0
    for i in range(len(s)):
        if sum(s[i:i + m]) == d:
            count += 1
    return count


def main():
    """
    Main function
    """

    _ = int(input().strip())
    s = list(map(int, input().rstrip().split()))

    first_multiple_input = input().rstrip().split()

    d = int(first_multiple_input[0])
    m = int(first_multiple_input[1])

    result = birthday(s, d, m)

    print(result)


if __name__ == '__main__':
    main()
