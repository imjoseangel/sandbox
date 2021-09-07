#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import math
import os
import random
import re
import sys


def main():
    N = int(input().strip())

    names = []

    for N_itr in range(N):
        first_multiple_input = input().rstrip().split()

        firstName = first_multiple_input[0]

        emailID = first_multiple_input[1]

        if re.search(r'@gmail\.com$', emailID):

            names.append(firstName)
            names.sort()

    print(*names, sep='\n')


if __name__ == '__main__':
    main()
