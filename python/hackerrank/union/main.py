#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    _ = int(input())
    a = set(map(int, input().split()))
    _ = int(input())
    b = set(map(int, input().split()))

    print(len(a.union(b)))


if __name__ == '__main__':
    main()
