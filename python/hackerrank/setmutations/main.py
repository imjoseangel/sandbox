#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    _ = int(input())
    A = set(map(int, input().split()))

    for _ in range(int(input())):

        command, _ = input().split()
        B = set(map(int, input().split()))

        getattr(A, command)(B)

    print(sum(A))


if __name__ == '__main__':
    main()
