#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def count_substring(string, sub_string):
    count = 0

    while sub_string in string:
        count += 1
        string = string[string.find(sub_string) + 1:]

    return count


if __name__ == '__main__':
    string = "ABCDCDC"
    sub_string = "CDC"

    count = count_substring(string, sub_string)
    assert count == 2
