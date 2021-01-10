#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import math
import os
import random
import re
import sys


# Complete the dayOfProgrammer function below.
def dayOfProgrammer(year):

    nofebcount = 31 + 31 + 30 + 31 + 30 + 31 + 31

    if year > 1918:
        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            yearcount = nofebcount + 29
        else:
            yearcount = nofebcount + 28

    elif year < 1918:
        if year % 4 == 0:
            yearcount = nofebcount + 29

        else:
            yearcount = nofebcount + 28
    else:
        yearcount = nofebcount + 15

    return "{0}.09.{1}".format(str(256 - yearcount), year)


if __name__ == '__main__':

    year = int(input().strip())
    result = dayOfProgrammer(year)

    print(result + '\n')
