#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def merge_the_tools(string, k):
    lenght = len(string)
    nk = int(lenght / k)

    chars = [string[index: index + nk]
             for index in range(0, len(string), nk)]
    print(list(chars))


def main():
    string = 'AABCAAADA'
    k = 3
    merge_the_tools(string, k)


if __name__ == '__main__':
    main()
