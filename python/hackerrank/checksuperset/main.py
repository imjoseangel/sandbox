#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    A = set(map(int, input().split()))

    print(all(A.issuperset(set(map(int, input().split())))
          for _ in range(int(input()))))


if __name__ == '__main__':
    main()
