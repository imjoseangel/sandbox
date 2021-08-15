#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    for _ in range(int(input())):
        s = input()

        print(s[::2], s[1::2])


if __name__ == '__main__':
    main()
