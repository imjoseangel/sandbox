#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    x, y = map(int, input().split())

    print(eval(input()) == y)


if __name__ == '__main__':
    main()
