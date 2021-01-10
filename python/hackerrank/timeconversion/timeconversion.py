#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


import os
import sys


def timeConversion(s):

    if s[-2:] == "PM":
        if s[:2] == "12":
            hour = "12"
        else:
            hour = str(int(s[:2]) + 12)
        return hour + s[2:8]
    elif s[:2] == "12":
        return "00" + s[2:8]
    else:
        return s[0:8]


if __name__ == '__main__':

    s = input()

    result = timeConversion(s)

    print(result + '\n')
