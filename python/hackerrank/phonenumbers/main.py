#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pattern for phone number.
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import re

PATTERN = r'^[7-9]\d{9}$'


def main():
    """
    Main function.
    """

    for _ in range(int(input())):
        phone_number = input()
        if re.match(PATTERN, phone_number):
            print('YES')
        else:
            print('NO')


if __name__ == '__main__':
    main()
