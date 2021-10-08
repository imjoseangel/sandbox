#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    a = int(input())
    b = map(int, input().split())
    c = int(input())
    d = map(int, input().split())

    print(len(set(b).symmetric_difference(set(d))))


if __name__ == '__main__':
    main()
