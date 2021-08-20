#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import itertools


def main():
    n = int(input().strip())

    z = [(item[0], len(list(item[1])))
         for item in itertools.groupby("{0:b}".format(n))]

    print(max(z, key=lambda item: item[1])[1])


if __name__ == '__main__':
    main()
