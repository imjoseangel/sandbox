#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal, getcontext


# @profile
def exp(x):
    getcontext().prec += 2
    i, lasts, s, fact, num = 0, 0, 1, 1, 1
    while s != lasts:
        lasts = s
        i += 1
        fact *= i
        num *= x
        s += num / fact
    getcontext().prec -= 2
    return +s


# @profile
def memory_intensive():
    small_list = [None] * 1000000
    big_list = [None] * 10000000
    del big_list
    return small_list


exp(Decimal(3000))
memory_intensive()
