#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from math import degrees, atan2


def main():

    AB = float(input())
    BC = float(input())

    degree_sign = u'\N{DEGREE SIGN}'
    print(f'{int(round(degrees(atan2(AB, BC))))}{degree_sign}')


if __name__ == '__main__':
    main()
