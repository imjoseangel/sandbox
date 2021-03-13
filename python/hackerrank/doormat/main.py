#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


CENTER = ".|."
SIDES = "-"
WELCOME = "WELCOME"


def drawdoor(n, m):

    middleline = round(n / 2) - 1
    middletext = int((m - len(WELCOME)) / 2)

    for item in range(0, n):
        if item == middleline:
            print(SIDES * middletext + WELCOME + SIDES * middletext)
        else:
            print(SIDES * m)


def main():
    drawdoor(11, 33)


if __name__ == '__main__':
    main()
