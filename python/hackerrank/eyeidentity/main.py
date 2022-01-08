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

    print(np.eye(N, M, k=0))


if __name__ == '__main__':
    main()
