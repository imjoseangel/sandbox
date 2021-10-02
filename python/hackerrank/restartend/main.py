#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import re


def main():
    S = str(input())
    k = str(input())

    m = re.search(k, S)
    if not m:
        print('(-1, -1)')
    else:
        print(f'({m.start()}, {m.end() - 1})')


if __name__ == '__main__':
    main()
