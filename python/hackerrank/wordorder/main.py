#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


from collections import Counter as counter


def main():
    n = int(input().rstrip())

    myset = list()

    for _ in range(0, n):
        myset.append(input().rstrip())

    print(len(set(myset)))
    qty = list(counter(myset).values())

    print(*qty, sep=" ")


if __name__ == '__main__':
    main()
