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

    if N % 2 != 0:
        print("Weird")
    elif N % 2 == 0 and N >= 2 and N <= 5:
        print("Not Weird")
    elif N % 2 == 0 and N >= 6 and N <= 20:
        print("Weird")
    else:
        print("Not Weird")


if __name__ == '__main__':
    main()
