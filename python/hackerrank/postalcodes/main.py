#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import re

regex_integer_in_range = r"^[1-9][0-9][0-9][0-9][0-9][0-9]$"
regex_alternating_repetitive_digit_pair = r"(\d)(?=\d\1)"


def main():

    try:
        P = input()
    except (ValueError, TypeError) as e:
        print(False)

    print(bool(re.match(regex_integer_in_range, P))
          and len(re.findall(regex_alternating_repetitive_digit_pair, P)) < 2)


if __name__ == '__main__':
    main()
