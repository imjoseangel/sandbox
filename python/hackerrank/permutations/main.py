#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from itertools import permutations
import string


def main():
    n, m = input().split()

    print(*[''.join(i) for i in permutations(sorted(n), int(m))], sep='\n')


if __name__ == '__main__':
    main()
