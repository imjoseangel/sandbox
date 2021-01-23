#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import sys
import re
import random
import os
import math


def kangaroo(x1, v1, x2, v2):

    k1 = map(lambda i: i, range(x1, 20000000, v1))
    k2 = map(lambda i: i, range(x2, 20000000, v2))

    for i, x in zip(k1, k2):
        if i == x:
            return "YES"
            break
    return "NO"


if __name__ == '__main__':

    # x1 = 4523
    # v1 = 8092
    # x2 = 9419
    # v2 = 8076

    x1 = 2081
    v1 = 8403
    x2 = 9107
    v2 = 8400

    # x1 = 0
    # v1 = 3
    # x2 = 4
    # v2 = 2

    result = kangaroo(x1, v1, x2, v2)
    print(result)
