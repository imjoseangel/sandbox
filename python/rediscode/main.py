#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
from timeit import default_timer as timer
from datetime import timedelta
import redis
import sys
import msgpack
from base64 import b64encode


def redisconnect(host="127.0.0.1", port=6379, password=""):

    rc = redis.Redis(host=host, port=port, password=password)
    return rc


def main():

    rc = redisconnect()
    pipe = rc.pipeline()

    key = 'key1Mb'
    xlsfile = open("excel.xls", "rb").read()

    value = msgpack.packb(xlsfile, use_bin_type=True)

    print(f'len of value = {sys.getsizeof(value)}')

    run(pipe, key, xlsfile)


def run(rc, key, value):
    start = timer()
    rc.mset({key: value})
    end = timer()
    print(timedelta(seconds=end - start))


if __name__ == '__main__':
    main()
