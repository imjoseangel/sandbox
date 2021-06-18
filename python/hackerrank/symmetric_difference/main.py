#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    sizea = input()
    arraya = set(map(int, input().rstrip().split()))
    sizeb = input()
    arrayb = set(map(int, input().rstrip().split()))

    myset = list(arraya.difference(arrayb))
    myset = myset + (list(arrayb.difference(arraya)))
    myset.sort()
    for item in myset:
        print(item)


if __name__ == '__main__':
    main()
