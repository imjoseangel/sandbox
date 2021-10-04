#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    dm = divmod(int(input()), int(input()))

    print(*dm, dm, sep="\n")


if __name__ == '__main__':
    main()
