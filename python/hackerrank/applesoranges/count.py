#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def countApplesAndOranges(s, t, a, b, apples, oranges):

    apples = [apple + a for apple in apples]
    oranges = [orange + b for orange in oranges]

    applesinrange = [apple for apple in apples if apple in range(s, t + 1)]
    print(len(applesinrange))

    orangesinrange = [
        orange for orange in oranges if orange in range(s, t + 1)]
    print(len(orangesinrange))


if __name__ == '__main__':

    st = [7, 11]

    s = int(st[0])

    t = int(st[1])

    ab = [5, 15]

    a = int(ab[0])

    b = int(ab[1])

    mn = [3, 2]

    m = int(mn[0])

    n = int(mn[1])

    apples = [-2, 2, 1]

    oranges = [5, -6]

    countApplesAndOranges(s, t, a, b, apples, oranges)
