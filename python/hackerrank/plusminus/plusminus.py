#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


import math
import os
import random
import re
import sys

# Complete the plusMinus function below.


def plusMinus(arr):
    positive = len([positive for positive in arr if positive > 0])
    negative = len([negative for negative in arr if negative < 0])
    zeroes = len([zeroes for zeroes in arr if zeroes == 0])

    formatted_output = "{:.6f}\n{:.6f}\n{:6f}".format(
        positive / n, negative / n, zeroes / n)

    print(formatted_output)


if __name__ == '__main__':
    n = int(input())

    arr = list(map(int, input().rstrip().split()))

    plusMinus(arr)
