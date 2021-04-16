#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from math import sqrt, pi, acos


def main():
    AB = 10
    c = 10
    CA = sqrt(AB**2 + c**2)

    b = CA / 2
    a = sqrt(b**2 + c**2)

    alpha = acos((b**2 + c**2 - a**2) / (2 * b * c))
    betta = acos((a**2 + c**2 - b**2) / (2 * a * c))
    gamma = acos((a**2 + b**2 - c**2) / (2 * a * b))

    alpha = alpha * 180 / pi
    betta = betta * 180 / pi
    gamma = gamma * 180 / pi

    print(alpha, betta, gamma)


if __name__ == '__main__':
    main()
