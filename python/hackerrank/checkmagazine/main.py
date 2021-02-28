#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from collections import Counter


def checkMagazine(magazine, note):

    return (Counter(note) - Counter(magazine)) == {}


if __name__ == '__main__':

    m = "two times three is not four"
    n = "two times is four"

    magazine = m.rstrip().split()
    note = n.rstrip().split()

    result = checkMagazine(magazine, note)
    if result:
        print("Yes")
    else:
        print("No")
