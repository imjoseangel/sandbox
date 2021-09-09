#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import math
import os
import random
import re
import sys


def median(nums):
    if len(nums) % 2 == 0:
        return (nums[len(nums) // 2 - 1] + nums[len(nums) // 2]) / 2
    else:
        return nums[len(nums) // 2]


def quartiles(arr):
    arr = sorted(arr)
    if len(arr) % 2 == 0:
        q1 = median(arr[:len(arr) // 2])
        q3 = median(arr[len(arr) // 2:])
    else:
        q1 = median(arr[:len(arr) // 2])
        q3 = median(arr[len(arr) // 2 + 1:])

    return sorted([int(q1), int(median(arr)), int(q3)])


def main():
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    data = list(map(int, input().rstrip().split()))

    res = quartiles(data)

    fptr.write('\n'.join(map(str, res)))
    fptr.write('\n')

    fptr.close()


if __name__ == '__main__':
    main()
