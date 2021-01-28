#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def findSubstring(s, k):

    maxvowel = 0
    finalstr = ""

    split = (s[item:item + k] for item in range(0, len(s), 1))

    mapofvowels = ((sum(
        list(map(mystr.lower().count, "aeiou"))), mystr) for mystr in split if len(mystr) == k)

    print(list(maximums))
    for count, word in mapofvowels:
        if count > maxvowel:
            maxvowel = count
            finalstr = word

        if finalstr == "":
            return "Not found!"

    return finalstr


if __name__ == '__main__':

    s = 'caberqiitefg'
    k = 5

    result = findSubstring(s, k)
    print(result)
