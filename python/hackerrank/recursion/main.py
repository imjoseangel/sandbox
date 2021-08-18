#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import math
import os
import random
import re
import sys


def factorial(n):

    for item in range(1, n):
        n = n * factorial(item)

    return n


def main():
    n = int(input().strip())
    result = factorial(n)

    print(str(result) + '\n')


if __name__ == '__main__':
    main()
