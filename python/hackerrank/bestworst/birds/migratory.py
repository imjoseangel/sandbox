#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def migratoryBirds(arr):

    maxcount = 0
    maxitem = 0

    for item in range(1, max(arr) + 1):
        print(maxitem)
        if arr.count(item) > maxcount:
            maxcount = arr.count(item)
            maxitem = item

    return maxitem


if __name__ == '__main__':

    arr = [1, 1, 2, 2, 3]
    result = migratoryBirds(arr)
    print(result)
