#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import re


def main():
    """
    Main function
    """
    for _ in range(int(input())):
        item = ''.join(sorted(input()))
        try:
            assert re.search(r'[A-Z]{2}', item)
            assert re.search(r'[0-9]{3}', item)
            assert not re.search(r'[^a-zA-Z0-9]', item)
            assert not re.search(r'(.)\1', item)
            assert len(item) == 10
        except AssertionError:
            print('Invalid')
        else:
            print('Valid')


if __name__ == '__main__':
    main()
