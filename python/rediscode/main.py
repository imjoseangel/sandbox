#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import gzip
from base64 import b64encode, b64decode
import json
from timeit import default_timer as timer
from datetime import timedelta
import logging
import os
import sys
import redis
from io import BytesIO
import msgpack


def compressStringToBytes(inputString):
    """
    read the given string, encode it in utf-8,
    compress the data and return it as a byte array.
    """
    bio = BytesIO()
    bio.write(inputString.encode("utf-8"))
    bio.seek(0)
    stream = BytesIO()
    compressor = gzip.GzipFile(fileobj=stream, mode='w')
    while True:  # until EOF
        chunk = bio.read(8192)
        if not chunk:  # EOF?
            compressor.close()
            return stream.getvalue()
        compressor.write(chunk)


def decompressBytesToString(inputBytes):
    """
    decompress the given byte array (which must be valid
    compressed gzip data) and return the decoded text (utf-8).
    """
    bio = BytesIO()
    stream = BytesIO(inputBytes)
    decompressor = gzip.GzipFile(fileobj=stream, mode='r')
    while True:  # until EOF
        chunk = decompressor.read(8192)
        if not chunk:
            decompressor.close()
            bio.seek(0)
            return bio.read().decode("utf-8")
        bio.write(chunk)
    return None


def generatefile(size):
    myfile = os.urandom(size)
    return myfile


def main():

    logging.basicConfig(format="%(asctime)s - %(message)s",
                        datefmt="%d-%b-%y %H:%M:%S", stream=sys.stderr, level=logging.DEBUG)

    redis_conn = redis.Redis(host="localhost", port=6380, db=0,
                             password=os.environ["REDISKEY"])

    key = '{HSS.NET_12p5w50wmcueoz5kbmd1tmzp}_Data'

    with open("file.json") as json_file:
        redisdata = json.load(json_file)

    # jsonpack = msgpack.packb(json.dumps(redisdata), use_bin_type=True)

    json_data = json.dumps(redisdata)

    # compressed = b64encode(gzip.compress(json.dumps(
    #     realvalue).encode('utf-8'))).decode('ascii')

    compressed = compressStringToBytes(json_data)

    logging.info(f'len of file = {sys.getsizeof(json_data)}')
    # logging.info(f'len of file = {sys.getsizeof(jsonpack)}')
    logging.info(f'len of file = {sys.getsizeof(compressed)}\n')

    redisset(redis_conn, key, json_data, "raw")
    redisget(redis_conn, key, "raw")

    redisset(redis_conn, key, compressed, "gzip")
    redisget(redis_conn, key, "gzip")


def redisset(redisconn, key, value, type):
    start = timer()

    for _ in range(1000):
        redisconn.set(key, value)

    end = timer()

    logging.info(f'Time set {type} = {timedelta(seconds=end - start)}')


def redisget(redisconn, key, type):

    start = timer()
    for _ in range(1000):
        redisconn.get(key)
    end = timer()

    logging.info(f'Time get {type} = {timedelta(seconds=end - start)}\n')


if __name__ == '__main__':
    main()
