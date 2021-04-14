#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from datetime import datetime
from calendar import month_abbr


def main():

    T = int(input().rstrip())

    for _ in range(0, T):
        day1, dd1, mm1, yyyy1, time1, diff1 = list(input().rstrip().split())
        day2, dd2, mm2, yyyy2, time2, diff2 = list(input().rstrip().split())

        date1 = datetime(year=int(yyyy1),
                         month=(list(month_abbr).index(mm1)),
                         day=int(dd1),
                         hour=int(time1.split(":")[0]),
                         minute=int(time1.split(":")[1]),
                         second=int(time1.split(":")[2]))

        date2 = datetime(year=int(yyyy2),
                         month=(list(month_abbr).index(mm2)),
                         day=int(dd2),
                         hour=int(time2.split(":")[0]),
                         minute=int(time2.split(":")[1]),
                         second=int(time2.split(":")[2]))

        difference = date1 - date2
        print(difference.days)


if __name__ == '__main__':
    main()
