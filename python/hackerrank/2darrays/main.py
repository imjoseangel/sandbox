#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    arr = []

    for _ in range(6):
        arr.append(list(map(int, input().rstrip().split())))


if __name__ == '__main__':
    main()
