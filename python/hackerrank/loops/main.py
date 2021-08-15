#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import math
import os
import random
import re
import sys


def main():
    n = int(input().strip())

    print('\n'.join(f'{n} x {item} = {n * item}' for item in range(1, 11)))


if __name__ == '__main__':
    main()
