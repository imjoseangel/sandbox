#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def prime(n: int) -> int:
    if n > 1:
        result = (i for i in range(2, n) if n % i == 0)

        try:
            next(result)
            return False
        except StopIteration:
            return True


def main():
    n = int(input())

    for _ in range(n):
        number = int(input())

        if prime(number):
            print("Prime")
        else:
            print("Not prime")


if __name__ == '__main__':
    main()
