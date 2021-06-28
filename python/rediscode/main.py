#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
import redis


def generatefile(size):
    myfile = os.urandom(size)
    return myfile


def redisconnect(host="127.0.0.1", port=6379, password=""):
    rc = redis.StrictRedis(host=host, port=port, password=password)
    return rc


def main():

    rc = redisconnect()
    pipe = rc.pipeline()

    key = 'key1Mb'
    value = generatefile(1048576)

    pipe.mset({key: value})
    pipe.execute()

    print(rc.get(key))


if __name__ == '__main__':
    main()
