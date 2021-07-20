#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    n, m = input().split()

    print(sum([max(map(int, input().split())) **
               2 for _ in range(int(n))]) % int(m))


if __name__ == '__main__':
    main()
