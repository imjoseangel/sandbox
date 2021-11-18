#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Validate email addresses
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import email.utils
import re


def main():
    """
    Main function
    """

    email_regex = re.compile(r"^[a-zA-Z][\w\-.]*@[a-zA-Z]+\.[a-zA-Z]{1,3}$")

    for _ in range(int(input())):
        address = input()
        if email_regex.match(email.utils.parseaddr(address)[1]):
            print(address)


if __name__ == '__main__':
    main()
