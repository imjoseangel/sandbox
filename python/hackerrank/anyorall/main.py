#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    _ = int(input())
    N = input().split()

    print(all(int(item) > 0 for item in N) and any(
        item == item[::-1] for item in N))


if __name__ == '__main__':
    main()
