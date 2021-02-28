#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import math
import os
import random
import re
import sys


# Complete the rotLeft function below.
def rotLeft(a, d):

    return a[d: len(a)] + a[0: d]


if __name__ == '__main__':

    d = 2
    a = [1, 2, 3, 4, 5]
    result = rotLeft(a, d)
    print(result)
