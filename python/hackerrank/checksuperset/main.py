#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    A = set(map(int, input().split()))

    superset = []

    for _ in range(int(input())):

        superset.append(A.issuperset(set(map(int, input().split()))))

    print(all(superset))


if __name__ == '__main__':
    main()
