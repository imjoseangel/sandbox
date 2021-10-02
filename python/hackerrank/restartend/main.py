#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import re


def main():
    S = input()
    k = input()

    pattern = re.compile(k)

    m = pattern.search(S)
    if not m:
        print('(-1, -1)')

    while m:
        print(f'({m.start()}, {m.end() - 1})')
        m = pattern.search(S, m.start() + 1)


if __name__ == '__main__':
    main()
