#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import ast


def main():
    T = int(input())

    for _ in range(T):
        try:
            print(isinstance(ast.literal_eval(input()), float))
        except (SyntaxError, ValueError):
            print('False')


if __name__ == '__main__':
    main()
