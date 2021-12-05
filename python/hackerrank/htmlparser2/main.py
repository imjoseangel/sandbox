#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    """ HTML Parser """


def main():
    """
    Main function
    """

    html = ""
    for _ in range(int(input())):
        html += input().rstrip()
        html += '\n'

    parser = MyHTMLParser()
    parser.feed(html)
    parser.close()


if __name__ == '__main__':
    main()
