#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


from itertools import chain, combinations
import regex


def minion_game(string):

    vowels = ['A', 'E', 'I', 'O', 'U']
    consnotwant = []
    vowelnotwant = []

    countcons = 0
    countvowel = 0

    combines = list(chain.from_iterable(combinations(string, r)
                                        for r in range(len(string) + 1)))

    middleresult = [''.join(combine) for combine in combines if combine]
    startcons = list(
        set([item for item in middleresult if item[0] not in vowels]))
    startvowel = set([item for item in middleresult if item[0] in vowels])

    for word in startcons:

        findcons = regex.findall(r'[^aeiou]+',
                                 word, regex.IGNORECASE)
        findvowel = regex.findall(r'[aeiou]+',
                                  word, regex.IGNORECASE)
        findword = findcons + findvowel

        for notcons in findword:
            if len(notcons) > 1:
                consnotwant.append(word)

    for word in startvowel:

        findcons = regex.findall(r'[^aeiou]+',
                                 word, regex.IGNORECASE)
        findvowel = regex.findall(r'[aeiou]+',
                                  word, regex.IGNORECASE)
        findword = findcons + findvowel

        for notvowel in findword:
            if len(notvowel) > 1:
                vowelnotwant.append(word)

    conslist = sorted(list(set(startcons) - set(consnotwant)))
    vowellist = sorted(list(set(startvowel) - set(vowelnotwant)))

    for letscountcons in conslist:
        countcons = countcons + \
            len(regex.findall(letscountcons, string, overlapped=True))

    for letscountvowel in vowellist:
        countvowel = countvowel + \
            len(regex.findall(letscountvowel, string, overlapped=True))

    if countcons > countvowel:
        print(f"Stuart {countcons}")
    else:
        print(f"Kevin {countvowel}")


def main():
    s = input()
    minion_game(s)


if __name__ == '__main__':
    main()
