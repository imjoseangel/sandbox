#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import string


def print_rangoli(size):
    rangoli = list(string.ascii_lowercase)

    middleline = rangoli[0:size][::-1] + rangoli[1:size]

    for i in range(2):
        middleline.pop(round(len(middleline) / 2))

    print('-'.join(middleline))


def main():
    print_rangoli(5)


if __name__ == '__main__':
    main()
