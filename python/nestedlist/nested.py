#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)


def main():
    records = []
    names = []
    scores = []
    for _ in range(int(input())):
        name = input()
        score = float(input())

        records.append([name, score])
        scores.append(score)

    mingrade = min(scores)
    secondgrade = max(scores)

    for item in records:
        if float(secondgrade) > float(item[1]) > float(mingrade):
            secondgrade = float(item[1])
            names = []
            names.append(str(item[0]))
        elif float(item[1]) == float(secondgrade):
            names.append(str(item[0]))

    for name in sorted(names):
        print(name)


if __name__ == '__main__':
    main()
