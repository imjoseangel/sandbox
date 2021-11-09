#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import re


def main():

    S = re.search(r'(\w(?!_))\1+', input())
    print(S.group(1) if S else -1)


if __name__ == '__main__':
    main()
