#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from collections import deque


def main():

    for _ in range(int(input())):

        _, a = int(input()), deque(map(int, input().split()))

        for cube in reversed(sorted(a)):

            if a[-1] == cube:
                a.pop()
            elif a[0] == cube:
                a.popleft()
            else:
                print('No')
                break
        else:
            print('Yes')


if __name__ == '__main__':
    main()
