#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from collections import Counter


def main():

    _ = int(input())
    n = [item for item, count in Counter(
        list(map(int, input().split()))).items() if count == 1]

    print(n[0])


if __name__ == '__main__':
    main()
