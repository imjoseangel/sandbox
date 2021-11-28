#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import requests
import resolver


def main():
    """
    Main function
    """

    resolver.bind_ip('www.example.com', 443, '216.58.215.174')

    # this sends requests to 216.58.215.174
    response = requests.get('https://www.example.com', verify=True)
    print(response.text)


if __name__ == '__main__':
    main()
