#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import dateutil.parser


def time_delta(t1, t2):

    date1 = dateutil.parser.parse(t1, fuzzy=True)
    date2 = dateutil.parser.parse(t2, fuzzy=True)

    diff = date2 - date1
    return str(int(abs(diff.total_seconds())))


def main():

    T = int(input().rstrip())

    for _ in range(0, T):

        t1 = input()
        t2 = input()

        delta = time_delta(t1, t2)
        print(delta + '\n')


if __name__ == '__main__':
    main()
