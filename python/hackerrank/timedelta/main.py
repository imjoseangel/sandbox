#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import datetime


def main():

    T = int(input().rstrip())

    for _ in range(0, T * 2):
        day, dd, mm, yyyy, time, diff = list(input().rstrip().split())

        print(dd)


if __name__ == '__main__':
    main()
