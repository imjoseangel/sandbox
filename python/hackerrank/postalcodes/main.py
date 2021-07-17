#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import re

regex_integer_in_range = r"^[1-9][0-9][0-9][0-9][0-9][0-9]$"


def main():

    try:
        P = input()
    except (ValueError, TypeError) as e:
        print(e)

    print(bool(re.match(regex_integer_in_range, P)))


if __name__ == '__main__':
    main()
