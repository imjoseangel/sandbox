#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    T = int(input())

    for _ in range(T):

        n = int(input())
        a = list(map(int, input().split()))

        print(a)


if __name__ == '__main__':
    main()
