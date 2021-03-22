#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


from collections import OrderedDict


def merge_the_tools(string, k):
    lenght = len(string)

    chars = [''.join(OrderedDict.fromkeys(string[index: index + k]))
             for index in range(0, lenght, k)]

    for item in list(chars):
        print(item)


def main():
    string = 'AABCAAADA'
    k = 3
    merge_the_tools(string, k)


if __name__ == '__main__':
    main()
