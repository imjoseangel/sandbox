#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import re


def main():
    pattern_match = r'^[456]\d{3}(-?\d{4}){3}$'
    consecutive_digits = r'(\d)\1{3}'

    n = int(input())

    for _ in range(n):
        credit_card = input()

        if re.match(pattern_match, credit_card) and not re.search(consecutive_digits, credit_card):
            print('Valid')
        else:
            print('Invalid')


if __name__ == '__main__':
    main()
