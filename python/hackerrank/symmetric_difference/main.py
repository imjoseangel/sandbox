#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    sizea = input()
    arraya = set(map(int, input().rstrip().split()))
    sizeb = input()
    arrayb = set(map(int, input().rstrip().split()))

    myseta = arraya.difference(arrayb)
    mysetb = arrayb.difference(arraya)
    mysetfinal = set(myseta.union(mysetb))

    print(*sorted(mysetfinal, key=int), sep='\n')


if __name__ == '__main__':
    main()
