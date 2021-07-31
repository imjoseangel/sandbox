#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    n = int(input().rstrip())

    myset = list()

    for _ in range(0, n):
        myset.append(input().rstrip())

    print(myset)


if __name__ == '__main__':
    main()
