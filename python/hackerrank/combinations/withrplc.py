#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from itertools import combinations_with_replacement


def main():
    s, n = input().strip().split()

    for item in combinations_with_replacement(sorted(s), int(n)):
        print(''.join(item))


if __name__ == '__main__':
    main()
