#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import string


def print_rangoli(size):
    rangoli = list(string.ascii_lowercase)
    rangolist = []

    middleline = rangoli[0:size][::-1] + rangoli[1:size]
    rangolilen = len('-'.join(middleline))

    rangolist.append(middleline[:])

    while len(middleline) > 1:
        for i in range(2):
            middleline.pop(round(len(middleline) / 2))

        rangolist.append(middleline[:])

    for item in rangolist[::-1]:
        print('-'.join(item).center(rangolilen, "-"))

    for item in rangolist:
        if item != rangoli[0:size][::-1] + rangoli[1:size]:
            print('-'.join(item).center(rangolilen, "-"))


def main():
    n = int(input())
    print_rangoli(n)


if __name__ == '__main__':
    main()
