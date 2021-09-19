#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    # More than 2 lines will result in 0 score. Do not leave a blank line also
    for i in range(1, int(input())):
        print(i * (10 ** i - 1) // 9)


if __name__ == '__main__':
    main()
