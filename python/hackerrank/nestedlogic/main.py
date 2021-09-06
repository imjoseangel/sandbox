#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from datetime import date, datetime


def main():
    rd, rm, ry = map(int, input().split())
    dd, dm, dy = map(int, input().split())

    datediff = datetime(ry, rm, rd) - datetime(dy, dm, dd)

    print(datediff)


if __name__ == '__main__':
    main()
