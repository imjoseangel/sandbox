#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from datetime import date, datetime


def main():
    rd, rm, ry = map(int, input().split())
    dd, dm, dy = map(int, input().split())

    datediff = datetime(ry, rm, rd) - datetime(dy, dm, dd)

    days = datediff.days
    months = (ry - dy) * 12 + rm - dm
    years = days // 365

    if years > 0:
        print(10000)
    elif months > 0:
        print(500 * months)
    else:
        print(15 * days)


if __name__ == '__main__':
    main()
