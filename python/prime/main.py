#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
First 40 primes
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import logging


def logger(msg):

    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO,
        datefmt="%d-%b-%y %H:%M:%S",
    )

    logging.info(msg)


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def main():

    for i in range(40):
        i = i**2 + i + 41

        logger(is_prime(i))


if __name__ == '__main__':
    main()
