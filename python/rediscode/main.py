#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import gzip
from timeit import default_timer as timer
from datetime import timedelta
import os
import sys
import redis
import msgpack


def generatefile(size):
    myfile = os.urandom(size)
    return myfile


def main():

    redis_conn = redis.Redis()

    key = 'key1Mb'
    xlsfile = open("excel.xls", "rb").read()

    print(xlsfile[0:20])

    value = msgpack.packb(gzip.compress(xlsfile))
    print(value[0:20])
    print(f'len of value = {sys.getsizeof(xlsfile)}')

    redisset(redis_conn, key, value)
    redisget(redis_conn, key)


def redisset(redisconn, key, value):
    start = timer()
    redisconn.mset({key: value})
    end = timer()
    print(timedelta(seconds=end - start))


def redisget(redisconn, key):

    start = timer()
    getkey = redisconn.get(key)
    end = timer()
    print(timedelta(seconds=end - start))
    print(getkey[0:20])
    value = gzip.decompress(msgpack.unpackb(getkey, raw=False))
    print(value[0:20])


if __name__ == '__main__':
    main()
