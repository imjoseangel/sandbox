#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from html.parser import HTMLParser


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print(f"Start : {tag}")
        if attrs:
            for attr in attrs:
                print(f"-> {attr[0]} > {attr[1]}")

    def handle_endtag(self, tag):
        print(f"End : {tag}")

    def handle_startendtag(self, tag, attrs):
        print(f"Empty : {tag}")


def main():

    # instantiate the parser and fed it some HTML
    parser = MyHTMLParser()
    parser.feed("<html><head><title>HTML Parser - I</title></head>"
                + "<body data-modal-target class='1'><h1>HackerRank</h1><br /></body></html>")


if __name__ == '__main__':
    main()
