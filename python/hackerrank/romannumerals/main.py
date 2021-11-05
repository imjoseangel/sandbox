#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import re


def main():
    regex_pattern = r"^M{,3}(C(D|M)|D?C{,3})(X(L|C)|L?X{,3})(I(X|V)|(X|V)?I{,3})$"
    print(str(bool(re.match(regex_pattern, input()))))


if __name__ == '__main__':
    main()
