#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def breakingRecords(scores):

    minscr = scores[0]
    maxscr = scores[0]
    mincount = 0
    maxcount = 0

    for score in scores:
        if score > maxscr:
            maxscr = score
            maxcount += 1
        elif score < minscr:
            minscr = score
            mincount += 1

    print(maxcount, mincount)


if __name__ == '__main__':

    scores = [3, 4, 21, 36, 10, 28, 35, 5, 24, 42]
    result = breakingRecords(scores)
