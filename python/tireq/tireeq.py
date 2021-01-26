#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import math


def tire(width, aspectratio, diameter):

    ratiobase = aspectratio / 100
    diameterbase = diameter * 25.4 / 2
    base = width * ratiobase
    ratio = diameterbase + base
    pi = math.pi
    perimeter = ratio * 2 * pi
    rounds = perimeter / 1000

    return rounds


def roundspercentage(tire1, tire2):

    base = (tire2 * 100) / tire1
    percentage = base - 100

    return percentage


def main():
    tire1 = tire(225, 60, 17)
    tire2 = tire(235, 55, 18)

    percentage = roundspercentage(tire1, tire2)

    print(" Tire 1: {:.2f} meters\n".format(round(tire1, 2)),
          "Tire 2: {:.2f} meters\n".format(round(tire2, 2)), "Difference: {:.2f}%".format(
              round(percentage, 2)))

    if percentage < 3.0:
        print("\n Equivalent")
    else:
        print("\n NOT Equivalent")


if __name__ == '__main__':
    main()
