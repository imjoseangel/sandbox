#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from collections import deque


def main():
    n = int(input())

    q = deque()

    for _ in range(n):
        command = input().split()
        if command[0] == 'append':
            q.append(int(command[1]))
        elif command[0] == 'appendleft':
            q.appendleft(int(command[1]))
        elif command[0] == 'pop':
            q.pop()
        elif command[0] == 'popleft':
            q.popleft()

    print(' '.join(map(str, q)))


if __name__ == '__main__':
    main()
