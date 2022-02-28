#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def sort_and_rotate(nums, k):
    nums.sort()
    for _ in range(0, k):
        nums.insert(0, nums.pop())
        print(nums)
    return nums


def main():
    """
    Main function
    """
    nums = [1, 2, 3, 4, 5, 6, 7]
    k = 7
    print(sort_and_rotate(nums, k))


if __name__ == '__main__':
    main()
