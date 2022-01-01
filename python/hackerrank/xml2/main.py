#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import xml.etree.ElementTree as etree

maxdepth = 0


def depth(elem, level):
    global maxdepth

    if (level == maxdepth):
        maxdepth += 1
   # recursive call to function to get the depth
    for child in elem:
        depth(child, level + 1)


def main():
    n = int(input())
    xml = ""
    for i in range(n):
        xml = xml + input() + "\n"
    tree = etree.ElementTree(etree.fromstring(xml))
    depth(tree.getroot(), -1)
    print(maxdepth)


if __name__ == '__main__':
    main()
