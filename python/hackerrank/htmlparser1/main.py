#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from html.parser import HTMLParser


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print("Found a start tag  :", tag)

    def handle_endtag(self, tag):
        print("Found an end tag   :", tag)

    def handle_startendtag(self, tag, attrs):
        print("Found an empty tag :", tag)


def main():

    # instantiate the parser and fed it some HTML
    parser = MyHTMLParser()
    parser.feed("<html><head><title>HTML Parser - I</title></head>"
                + "<body><h1>HackerRank</h1><br /></body></html>")


if __name__ == '__main__':
    main()
