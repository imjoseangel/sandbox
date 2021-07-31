#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from itertools import groupby


def main():

    S = input()
    groups = groupby(S)

    print(list(groups))


if __name__ == '__main__':
    main()
