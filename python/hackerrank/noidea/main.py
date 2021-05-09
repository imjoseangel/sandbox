#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    _ = input()
    array = list(input().rstrip())
    a = set(input().split())
    b = set(input().split())
    initial = 0

    for item in array:
        if item in a:
            initial += 1
        elif item in b:
            initial -= 1

    print(initial)


if __name__ == '__main__':
    main()
