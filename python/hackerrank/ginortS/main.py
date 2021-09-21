#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import re


def main():
    n = input()

    textlow = re.sub(r'[^a-z]', '', n)
    textupp = re.sub(r'[^A-Z]', '', n)
    numbers = re.sub(r'[a-zA-Z]', '', n)

    print("".join(sorted(textlow)) +
          "".join(sorted(textupp)) + "".join(sorted(numbers, key=lambda x: [int(x) % 2 == 0, x])))


if __name__ == '__main__':
    main()
