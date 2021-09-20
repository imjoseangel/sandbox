#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


class EvenStream(object):
    def __init__(self):
        self.current = 0

    def get_next(self):
        to_return = self.current
        self.current += 2
        return to_return


class OddStream(object):
    def __init__(self):
        self.current = 1

    def get_next(self):
        to_return = self.current
        self.current += 2
        return to_return


def print_from_stream(n, stream=EvenStream()):
    stream.__init__()
    for _ in range(n):
        print(stream.get_next())


def main():

    queries = int(input())
    for _ in range(queries):
        stream_name, n = input().split()
        n = int(n)
        if stream_name == "even":
            print_from_stream(n)
        else:
            print_from_stream(n, OddStream())


if __name__ == '__main__':
    main()
