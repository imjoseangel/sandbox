#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    k, m = map(int, input().split())

    sum(max(map(int, input().split())) ** 2 for _ in range(k))


if __name__ == '__main__':
    main()
