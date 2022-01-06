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
    nums = tuple(map(int, input().split()))

    print(np.zeros(nums, dtype=np.int32))
    print(np.ones(nums, dtype=np.int32))


if __name__ == '__main__':
    main()
