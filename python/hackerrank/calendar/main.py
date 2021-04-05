#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import calendar


def main():
    print(calendar.TextCalendar(firstweekday=6).formatyear(2015))


if __name__ == '__main__':
    main()
