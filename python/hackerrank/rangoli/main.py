#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import string


def print_rangoli(size):
    rangoli = list(string.ascii_lowercase)
    print(rangoli[0:3][::-1])


def main():
    print_rangoli(3)


if __name__ == '__main__':
    main()
