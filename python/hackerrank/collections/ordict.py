#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from collections import OrderedDict


def main():

    Items = OrderedDict()

    for _ in range(int(input())):

        name, _, price = input().rpartition(' ')
        Items[name] = Items.get(name, 0) + int(price)

    for item, quantity in Items.items():
        print(item, quantity)


if __name__ == '__main__':
    main()
