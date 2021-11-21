#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import re


def main():

    hexcolor = re.compile(r'#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})')
    hexfound = []

    for _ in range(int(input())):
        line = input()

        if not line.startswith('#'):
            hexfound.extend(re.findall(hexcolor, line))

    print('\n'.join([f'#{hexcolor}' for hexcolor in hexfound]))


if __name__ == '__main__':
    main()
