#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from itertools import groupby


def main():
    s = input()
    for k, g in groupby(s):
        print(f'({len(list(g))}, {k})', end=' ')


if __name__ == '__main__':
    main()
