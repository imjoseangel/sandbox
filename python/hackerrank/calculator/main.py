#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


class Calculator():

    def power(self, n, p):
        if n < 0 or p < 0:
            raise Exception('n and p should be non-negative')
        else:
            return n**p


def main():

    myCalculator = Calculator()

    T = int(input())
    for i in range(T):
        n, p = map(int, input().split())
        try:
            ans = myCalculator.power(n, p)
            print(ans)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
