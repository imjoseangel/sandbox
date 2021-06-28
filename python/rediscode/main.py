#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
import redis


def generatefile(size):
    myfile = os.urandom(size)
    return myfile


def main():
    redischunk = generatefile(1048576)


if __name__ == '__main__':
    main()
