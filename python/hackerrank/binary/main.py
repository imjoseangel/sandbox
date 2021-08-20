#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import itertools


def main():
    n = int(input().strip())

    for i in "{0:b}".format(n):
        print(i)


if __name__ == '__main__':
    main()
