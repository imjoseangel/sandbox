#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from collections import namedtuple


def main():
    student = namedtuple('student', 'ID MARKS CLASS NAME')

    total = int(input().rstrip())
    fields = list(input().split())

    marksum = 0

    for _ in range(0, total):
        tempsum = list(input().rstrip().split())
        marksum += int(tempsum[fields.index('MARKS')])

    print(f"{marksum / total:.2f}")


if __name__ == '__main__':
    main()
