#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import re


def main():
    S = str(input())
    k = str(input())

    m = re.search(k, S)

    print(m.end(), m.start())


if __name__ == '__main__':
    main()
