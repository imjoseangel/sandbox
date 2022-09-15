#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dis
from math import e


def exp(x):
    return e**x  # math.exp(x)


dis.dis(exp)
