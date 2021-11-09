#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import re


def main():
    S = input()

    result = re.search(r'(\w(?!_))\1+', S)
    print(result.group(1) if result else -1)


if __name__ == '__main__':
    main()
