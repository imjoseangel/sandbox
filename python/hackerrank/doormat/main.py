#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import math

CENTER = ".|."
SIDES = "-"
WELCOME = "WELCOME"


def drawdoor(n, m):

    middleline = math.ceil(n / 2)
    middletext = int((m - len(WELCOME)) / 2)

    for item in range(1, n + 1):
        if item == middleline:
            print(SIDES * middletext + WELCOME + SIDES * middletext)
        elif item < middleline:
            middleitem = CENTER * (2 * item - 1)
            middledash = int((m - len(middleitem)) / 2)
            print((SIDES * middledash) + middleitem + (SIDES * middledash))
        else:
            middleitem = CENTER * (n - (2 * (item - middleline)))
            middledash = int((m - len(middleitem)) / 2)
            print((SIDES * middledash) + middleitem + (SIDES * middledash))


def main():
    n, m = map(int, input().split())
    drawdoor(n, m)


if __name__ == '__main__':
    main()
