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
    N, M = map(int, input().split())
    np.set_printoptions(legacy='1.13')
    print(np.eye(N, M))


if __name__ == '__main__':
    main()
