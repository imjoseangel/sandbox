#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


class AdvancedArithmetic(object):
    def divisorSum(n):
        raise NotImplementedError


class Calculator(AdvancedArithmetic):
    def divisorSum(self, n):
        pass


def main():

    n = int(input())
    my_calculator = Calculator()
    s = my_calculator.divisorSum(n)
    print("I implemented: " + type(my_calculator).__bases__[0].__name__)
    print(s)


if __name__ == '__main__':
    main()
