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

    n, _ = map(int, input().split())
    a = np.array([input().split() for _ in range(n)], int)
    print(a.transpose())
    print(a.flatten())


if __name__ == '__main__':
    main()
