#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    _ = input()
    array = list(input().rstrip())
    a = set(input().split())
    b = set(input().split())

    print(sum((item in a) - (item in b) for item in array))


if __name__ == '__main__':
    main()
