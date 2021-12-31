#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import sys
import xml.etree.ElementTree as etree


def get_attr_number(node):
    """
    Get the number of attributes of a node
    """
    return len(node.attrib) + sum(get_attr_number(child) for child in node)


def main():
    """
    Main function
    """
    sys.stdin.readline()
    xml = sys.stdin.read()
    tree = etree.ElementTree(etree.fromstring(xml))
    root = tree.getroot()
    print(get_attr_number(root))


if __name__ == '__main__':
    main()
