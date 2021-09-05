#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def prime(n: int) -> int:

    if n == 1:
        return False
    else:
        if n % 2 == 0 and n > 2:
            return False
        else:
            for i in range(3, int(n**(1 / 2)) + 1, 2):
                if n % i == 0:
                    return False
            else:
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
