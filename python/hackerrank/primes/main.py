#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    n = int(input())

    for _ in range(n):
        number = int(input())

        x = (i for i in range(2, number) if number % i == 0)

        try:
            next(x)
            print('Not prime')
        except StopIteration:
            print('Prime')


if __name__ == '__main__':
    main()
