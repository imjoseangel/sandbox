#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def findSubstring(s, k):

    maxvowel = 0

    # split = (s[item:item + k] for item in range(0, len(s), 1))

    # mapofvowels = ((sum(
    #     list(map(mystr.lower().count, "aeiou"))), mystr) for mystr in split if len(mystr) == k)

    # [(maxvowel := count, finalstr := word) for count, word in mapofvowels
    #  if count > maxvowel]

    findstr = ((maxvowel := count, word) for count, word in ((sum(
        list(map(mystr.lower().count, "aeiou"))), mystr) for mystr in (s[item:item + k] for item in range(0, len(s), 1)) if len(mystr) == k)
        if count > maxvowel)

    try:
        result = (max(findstr)[1])
        return result
    except ValueError:
        return "Not found!"


if __name__ == '__main__':

    s = 'caberqiitefg'
    k = 5

    result = findSubstring(s, k)
    print(result)
