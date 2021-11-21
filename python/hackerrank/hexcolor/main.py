#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import regex


def main():

    N = int(input())

    hexcolor = regex.compile(r'#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})')
    hexfound = []

    for _ in range(N):
        hexfound.extend(regex.findall(hexcolor, input()))

    print('\n'.join(hexfound))


if __name__ == '__main__':
    main()
