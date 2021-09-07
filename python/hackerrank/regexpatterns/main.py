#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import re


def main():
    N = int(input().strip())

    names = []

    for _ in range(N):
        first_multiple_input = input().rstrip().split()
        firstName = first_multiple_input[0]
        emailID = first_multiple_input[1]

        if re.search(r'@gmail\.com$', emailID):
            names.append(firstName)

    print(*sorted(names), sep='\n')


if __name__ == '__main__':
    main()
