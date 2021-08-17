#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    n = int(input())

    phoneBook = {key: value for key, value in [
        input().rstrip().split() for _ in range(0, n)]}

    for _ in range(0, n):
        name = input()
        if name in phoneBook:
            print(name + "=" + phoneBook[name])
        else:
            print("Not found")


if __name__ == '__main__':
    main()
