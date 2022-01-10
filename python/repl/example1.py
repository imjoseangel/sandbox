#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import requests
import ipdb


def make_requests():
    result = requests.get('http://www.google.com')
    ipdb.set_trace()


def main():
    """
    Main function
    """
    make_requests()


if __name__ == '__main__':
    main()
