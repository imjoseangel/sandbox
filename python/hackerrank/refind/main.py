#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Re.findall() & Re.finditer() from hackerrank
"""
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import re


def main():
    """
    You are given a string . It consists of alphanumeric characters, spaces and symbols(+,-).
    Your task is to find all the substrings of  that contains  or more vowels.
    Also, these substrings must lie in between  consonants and should contain vowels only.
    """

    # Read input
    S = re.findall(r'(?<=[^aeiouAEIOU])([aeiouAEUIO]{2,})[^aeiou]', input())

    # Print output
    if S:
        print('\n'.join(S))
    else:
        print('-1')


if __name__ == '__main__':
    main()
