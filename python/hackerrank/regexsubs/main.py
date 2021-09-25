#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import re


def replandor(match):
    if match.group() == "&&":
        return "and"
    else:
        return "or"


def main():
    n = int(input())

    for _ in range(n):
        s = input()
        print(re.sub(r"(?<= )(&&|\|\|)(?= )", replandor, s))


if __name__ == '__main__':
    main()
