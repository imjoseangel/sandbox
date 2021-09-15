#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from collections import Counter


def main():
    n = input()

    print(Counter(sorted(n)))


if __name__ == '__main__':
    main()
