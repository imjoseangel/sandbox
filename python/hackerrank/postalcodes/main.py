#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import re


def main():

    try:
        p = int(input())
    except (ValueError, TypeError) as e:
        print(e)

    if not 100000 <= p <= 999999:
        print("False")


if __name__ == '__main__':
    main()
