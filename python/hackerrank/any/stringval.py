#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    s = input()
    print(any(item.isalnum() for item in s))
    print(any(item.isalpha() for item in s))
    print(any(item.isdigit() for item in s))
    print(any(item.islower() for item in s))
    print(any(item.isupper() for item in s))


if __name__ == '__main__':
    main()
