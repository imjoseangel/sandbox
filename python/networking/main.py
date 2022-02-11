#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from scapy.all import *


def main():
    """
    Main function
    """
    send(IP(dst="1.2.3.4") / TCP(dport=502, options=[("MSS", 0)]))


if __name__ == '__main__':
    main()
