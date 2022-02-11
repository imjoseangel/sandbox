#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from scapy.all import Ether, IP, TCP
from scapy.contrib.macsec import MACsec


def main():
    """
    Main function
    """
    p = Ether() / IP(dst="www.secdev.org") / TCP()
    print(p.summary())
    print(p.show())


if __name__ == '__main__':
    main()
