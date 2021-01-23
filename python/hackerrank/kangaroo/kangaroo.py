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

    k1 = enumerate([item for item in range(x1, 10000, v1)])
    k2 = enumerate([item for item in range(x2, 10000, v2)])

    final = set(k1) & set(k2)

    if final:
        print("YES")
    else:
        print("NO")


if __name__ == '__main__':

    x1 = 2
    v1 = 1
    x2 = 1
    v2 = 2

    result = kangaroo(x1, v1, x2, v2)
