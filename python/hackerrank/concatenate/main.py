#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import numpy as np


def main():
    """
    Main function
    """
    n, m, p = map(int, input().split())

    a = np.array([input().split() for _ in range(n + m)], int)

    print(a)


if __name__ == '__main__':
    main()
