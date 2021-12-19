#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    """
    Main function
    """
    n = 18
    x = ((' ' * (n - (item + 1)), '*' * (2 * item + 1)) for item in range(n))
    for item in x:
        print(item[0] + item[1])


if __name__ == '__main__':
    main()
