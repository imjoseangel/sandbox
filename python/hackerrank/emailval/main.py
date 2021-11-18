#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Validate email addresses
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import email.utils


def main():
    """
    Main function
    """

    for _ in range(int(input())):
        print(email.utils.parseaddr(input())[1])


if __name__ == '__main__':
    main()
