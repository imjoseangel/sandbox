#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    T = int(input().rstrip())
    for _ in range(0, T):
        m, n = input().split()
        try:
            print(int(m) // int(n))
        except BaseException as err:
            print(f"Error Code: {err}")


if __name__ == '__main__':
    main()
