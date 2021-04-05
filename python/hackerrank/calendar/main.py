#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import calendar


def main():

    weekdays = ["MONDAY", "TUESDAY",
                "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
    month, day, year = map(int, input().rstrip().split())
    print(weekdays[calendar.weekday(year, month, day)])


if __name__ == '__main__':
    main()
