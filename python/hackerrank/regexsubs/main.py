#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    n = int(input())

    for i in range(n):
        s = input()

        print(s.replace(' || ', ' or ').replace(' && ', ' and '))


if __name__ == '__main__':
    main()
