#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


from itertools import chain, combinations
import re


def minion_game(string):

    vowels = ['A', 'E', 'I', 'O', 'U']
    consnotwant = []

    combines = list(chain.from_iterable(combinations(string, r)
                                        for r in range(len(string) + 1)))

    middleresult = [''.join(combine) for combine in combines if combine]
    startcons = list(
        set([item for item in middleresult if item[0] not in vowels]))
    startvowel = set([item for item in middleresult if item[0] in vowels])

    for word in startcons:

        findcons = re.findall(r'[^aeiou]+',
                              word, re.IGNORECASE)
        findvowel = re.findall(r'[aeiou]+',
                               word, re.IGNORECASE)
        findword = findcons + findvowel

        for notcons in findword:
            if len(notcons) > 1:
                consnotwant.append(word)

    conslist = (list(set(startcons) - set(consnotwant)))
    print(conslist)


def main():
    # s = input()
    s = 'BANANA'
    minion_game(s)


if __name__ == '__main__':
    main()
