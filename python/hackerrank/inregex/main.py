#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import re


def main():

    T = int(input().rstrip())
    for _ in range(0, T):
        try:
            re.compile(input())
            print(True)
        except re.error:
            print(False)


if __name__ == '__main__':
    main()
