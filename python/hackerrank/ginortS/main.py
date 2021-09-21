#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import re


def main():
    n = input()

    text = re.sub(r'[^a-zA-Z]', '', n)
    numb = re.sub(r'[a-zA-Z]', '', n)

    print(f"{text[::-1]}{numb}")


if __name__ == '__main__':
    main()
