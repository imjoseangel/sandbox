#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from cmath import phase


def main():

    Y = complex(input().rstrip())

    print(abs(complex(Y.real, Y.imag)))
    print(phase(complex(Y.real, Y.imag)))


if __name__ == '__main__':
    main()
