#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from collections import Counter


def main():
    n = input()

    for a, b in Counter(sorted(n)).most_common(3):
        print(a, b)


if __name__ == '__main__':
    main()
