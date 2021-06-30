#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import gzip
from timeit import default_timer as timer
from datetime import timedelta
import logging
import os
import sys
import redis
import msgpack


def generatefile(size):
    myfile = os.urandom(size)
    return myfile


def main():

    logging.basicConfig(format="%(asctime)s - %(message)s",
                        datefmt="%d-%b-%y %H:%M:%S", stream=sys.stderr, level=logging.DEBUG)

    redis_conn = redis.Redis(host="localhost", port=6380, db=0,
                             password=os.environ["REDISKEY"])

    key = 'key1Mb'
    xlsfile = open("excel.xls", "rb").read()

    valuepack = msgpack.packb(xlsfile)
    valuegzip = gzip.compress(xlsfile)
    valuepackgzip = msgpack.packb(gzip.compress(xlsfile), use_bin_type=True)

    logging.info(f'len of file = {sys.getsizeof(xlsfile)}\n')

    logging.info(f'xlsfile = {xlsfile[0:20]}')
    logging.info(f'valuepack = {valuepack[0:20]}')
    logging.info(f'valuegzip = {valuegzip[0:20]}')
    logging.info(f'valuepackgzip = {valuepackgzip[0:20]}\n')

    redisset(redis_conn, key, xlsfile, "raw")
    redisget(redis_conn, key, "raw")

    redisset(redis_conn, key, valuepack, "msgpack")
    redisget(redis_conn, key, "msgpack")

    redisset(redis_conn, key, valuegzip, "gzip")
    redisget(redis_conn, key, "gzip")

    redisset(redis_conn, key, valuepackgzip, "msgpack+gzip")
    redisget(redis_conn, key, "msgpack+gzip")


def redisset(redisconn, key, value, type):
    start = timer()
    redisconn.mset({key: value})
    end = timer()

    logging.info(f'Time set {type} = {timedelta(seconds=end - start)}')


def redisget(redisconn, key, type):

    start = timer()
    getkey = redisconn.get(key)
    end = timer()

    logging.info(f'Time get {type} = {timedelta(seconds=end - start)}\n')
    logging.info(f'value = {getkey[0:20]}\n')

    try:
        # value = gzip.decompress(msgpack.unpackb(getkey, raw=False))
        value = gzip.decompress(getkey)
        # value = msgpack.unpackb(getkey, raw=False)
        logging.info(f'value = {value[0:20]}\n')
    except msgpack.exceptions.ExtraData as e:
        pass
    except gzip.BadGzipFile as e:
        pass


if __name__ == '__main__':
    main()
