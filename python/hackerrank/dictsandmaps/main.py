#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    n = int(input())

    for _ in range(0, n):
        s = zip(input().rstrip().split())

        print(dict(s))


if __name__ == '__main__':
    main()
