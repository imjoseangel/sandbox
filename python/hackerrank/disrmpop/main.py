#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():

    n = int(input())
    s = set(map(int, input().split()))

    x = int(input())

    for _ in range(x):
        command = input().split()
        if command[0] == 'pop':
            s.pop()
        elif command[0] == 'remove':
            s.remove(int(command[1]))
        elif command[0] == 'discard':
            s.discard(int(command[1]))

    print(sum(s))


if __name__ == '__main__':
    main()
