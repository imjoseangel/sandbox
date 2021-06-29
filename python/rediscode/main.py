#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
from timeit import timeit
import redis


def generatefile(size):
    myfile = os.urandom(size)
    return myfile


def redisconnect(host="127.0.0.1", port=6379, password=""):

    rc = redis.Redis(host=host, port=port, password=password)
    return rc


def main():

    rc = redisconnect()
    pipe = rc.pipeline()

    key = 'key1Mb'
    value = generatefile(104857699)

    print(timeit(f'{runnotpipe(pipe, key, value)}'))
    print(timeit(f'{run(pipe, key, value)}'))


def runnotpipe(rc, key, value):
    rc.mset({key: value})


def run(pipe, key, value):

    pipe.mset({key: value})
    pipe.execute()


if __name__ == '__main__':
    main()
