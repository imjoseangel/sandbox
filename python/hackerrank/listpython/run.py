#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    N = int(input())

    lis = []
    for _ in range(N):
        command, *value = input().split()
        if command == 'print':
            print(lis)
        else:
            print(*(map(int, value)))
            # getattr(lis, command)(*(map(int, value)))


if __name__ == '__main__':
    main()
