#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


from itertools import chain, combinations
import re


def minion_game(string):

    vowels = 'AEIOU'

    kevsc = 0
    stusc = 0
    for i in range(len(string)):
        if string[i] in vowels:
            kevsc += (len(string) - i)
        else:
            stusc += (len(string) - i)

    if kevsc > stusc:
        print("Kevin", kevsc)
    elif kevsc < stusc:
        print("Stuart", stusc)
    else:
        print("Draw")


def main():
    # s = input()
    s = 'BANANA'
    minion_game(s)


if __name__ == '__main__':
    main()
