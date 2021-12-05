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

    def handle_comment(self, data):
        """
        :param data:
        :return:
        """
        if '\n' in data:
            print('>>> Multi-line Comment')
        else:
            print('>>> Single-line Comment')
        print(data)

    def handle_data(self, data):
        """
        :param data:
        :return:
        """
        if data.strip():
            print('>>> Data')
            print(data)


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
