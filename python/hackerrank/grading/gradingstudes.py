#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def gradingStudents(grades):

    base = 5
    finalgrades = []

    for grade in grades:
        nearest_multiple = base * round(grade / base)

        if grade < 38 or nearest_multiple < grade:
            finalgrades.append(grade)
        else:
            finalgrades.append(nearest_multiple)

    return finalgrades


if __name__ == '__main__':

    grades = [73, 67, 38, 33]
    result = gradingStudents(grades)
    print(result)
