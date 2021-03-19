#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


from itertools import chain, combinations


def minion_game(string):

    vowels = ['A', 'E', 'I', 'O', 'U']
    finalcons = []
    finalvowel = []
    letters = list(string)

    combines = list(chain.from_iterable(combinations(string, r)
                                        for r in range(len(string) + 1)))

    middleresult = [''.join(combine) for combine in combines if combine]
    startcons = [item for item in middleresult if item[0]
                 not in vowels]
    startvowel = [item for item in middleresult if item[0] in vowels]

    for item in set(startcons):
        print(item)


def main():
    # s = input()
    s = 'BANANA'
    minion_game(s)


if __name__ == '__main__':
    main()
