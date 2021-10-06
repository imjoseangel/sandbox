#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    a, b, c, d = (int(input()) for _ in range(4))

    print(pow(a, b) + pow(c, d))


if __name__ == '__main__':
    main()
