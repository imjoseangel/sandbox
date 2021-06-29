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

    value = msgpack.packb(gzip.compress(xlsfile), use_bin_type=True)
    print(f'len of value = {sys.getsizeof(xlsfile)}')

    set(rc, key, value)


def set(rc, key, value):
    start = timer()
    rc.mset({key: value})
    end = timer()
    print(timedelta(seconds=end - start))


def get(rc, key):

    start = timer()
    rc.get(key)
    end = timer()
    print(timedelta(seconds=end - start))


if __name__ == '__main__':
    main()
