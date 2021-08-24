#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


class Difference:
    def __init__(self, a):
        self.__elements = a

    def computeDifference(self):
        self.maximumDifference = 0
        for i in range(len(self.__elements)):
            for j in range(i + 1, len(self.__elements)):
                if abs(self.__elements[i] - self.__elements[j]) > self.maximumDifference:
                    self.maximumDifference = abs(
                        self.__elements[i] - self.__elements[j])


def main():

    _ = input()
    a = [int(e) for e in input().split(' ')]

    d = Difference(a)
    d.computeDifference()

    print(d.maximumDifference)


if __name__ == '__main__':
    main()
