#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import re


def main():
    n = input()

    print("".join(sorted(re.sub(r'[^a-z]', '', n))) +
          "".join(sorted(re.sub(r'[^A-Z]', '', n))) +
          "".join(sorted(re.sub(r'[a-zA-Z]', '', n),
                         key=lambda x: [int(x) % 2 == 0, x])))


if __name__ == '__main__':
    main()
