#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print(f"Start : {tag}")
        if attrs:
            for attr in attrs:
                print(f"-> {attr[0]} > {attr[1]}")

    def handle_endtag(self, tag):
        print(f"End   : {tag}")

    def handle_startendtag(self, tag, attrs):
        print(f"Empty : {tag}")


def main():

    # instantiate the parser and fed it some HTML
    parser = MyHTMLParser()

    for _ in range(int(input())):
        parser.feed(input())


if __name__ == '__main__':
    main()
