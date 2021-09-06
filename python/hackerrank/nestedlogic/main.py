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
    years = ry - dy

    if years > 0:
        print(10000)
    elif months > 0:
        print(500 * months)
    elif days > 0:
        print(15 * days)
    else:
        print(0)


if __name__ == '__main__':
    main()
