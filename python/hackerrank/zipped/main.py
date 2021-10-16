#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    A = []

    for _ in range(list(map(int, input().rstrip().split()))[1]):
        A.append(input().rstrip().split())

    print(*[sum(list(map(float, item))) / len(item)
          for item in list(zip(*A))], sep='\n')


if __name__ == '__main__':
    main()
