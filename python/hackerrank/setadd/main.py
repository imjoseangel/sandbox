#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    myset = set()
    n = int(input())

    for _ in range(1, n + 1):
        myset.add(input())

    print(len(myset))


if __name__ == '__main__':
    main()
