#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


from itertools import chain, combinations
import re


def minion_game(string):

    vowels = 'AEIOU'

    kevsc, stusc = 0, 0
    length = len(string)

    for item in range(length):

        score = length - item

        if string[item] in vowels:
            kevsc += score
        else:
            stusc += score

    if kevsc > stusc:
        print(f"Kevin {kevsc}")
    elif kevsc < stusc:
        print(f"Stuart {stusc}")
    else:
        print("Draw")


def main():
    # s = input()
    s = 'BANANA'
    minion_game(s)


if __name__ == '__main__':
    main()
