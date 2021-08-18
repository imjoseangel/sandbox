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

    return n * factorial(n - 1) if n > 1 else 1


def main():
    n = int(input().strip())
    result = factorial(n)

    print(str(result) + '\n')


if __name__ == '__main__':
    main()
