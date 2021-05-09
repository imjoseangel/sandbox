#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    m = 3
    n = 2
    array = [1, 5, 3]
    a = (3, 1)
    b = (5, 7)
    initial = 0

    for item in array:
        if item in a:
            initial += 1
        elif item in b:
            initial -= 1

    print(initial)


if __name__ == '__main__':
    main()
