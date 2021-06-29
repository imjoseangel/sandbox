#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import zlib
import gzip
from timeit import default_timer as timer
from datetime import timedelta
import redis
import sys
import msgpack
from base64 import b64encode


def main():

    rc = redis.Redis()

    key = 'key1Mb'
    xlsfile = open("excel.xls", "rb").read()

    print(xlsfile[0:20])

    value = msgpack.packb(gzip.compress(xlsfile), use_bin_type=True)
    print(value[0:20])
    print(f'len of value = {sys.getsizeof(xlsfile)}')

    set(rc, key, value)
    get(rc, key)


def set(rc, key, value):
    start = timer()
    rc.mset({key: value})
    end = timer()
    print(timedelta(seconds=end - start))


def get(rc, key):

    start = timer()
    x = rc.get(key)
    end = timer()
    print(timedelta(seconds=end - start))
    print(x[0:20])
    value = gzip.decompress(msgpack.unpackb(x, raw=False))
    print(value[0:20])


if __name__ == '__main__':
    main()
