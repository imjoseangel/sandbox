#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    n = int(input().strip())

    arr = list(map(int, input().rstrip().split()))

    print(" ".join(map(str, arr[::-1])))


if __name__ == '__main__':
    main()
