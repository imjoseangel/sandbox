#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
import redis


def time_this(original_function):
    def timer(*args, **kwargs):
        import datetime
        before = datetime.datetime.now()
        time = original_function(*args, **kwargs)
        after = datetime.datetime.now()
        print("Elapsed Time = {0}".format(after - before))
        return time

    return timer


def generatefile(size):
    myfile = os.urandom(size)
    return myfile


def redisconnect(host="127.0.0.1", port=6379, password=""):

    rc = redis.Redis(host=host, port=port, password=password)
    return rc


@time_this
def main():

    rc = redisconnect()
    pipe = rc.pipeline()

    key = 'key1Mb'
    value = generatefile(104857699)

    runnotpipe(rc, key, value)
#    run(pipe, key, value)


@time_this
def runnotpipe(rc, key, value):
    rc.mset({key: value})


@time_this
def run(pipe, key, value):
    pipe.mset({key: value})
    pipe.execute()


if __name__ == '__main__':
    main()
