#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from prometheus_client import Summary

import scapy.all as scapy
from scapy.layers.inet import Ether
from scapy.contrib.macsec import MACsec
from scapy.layers.inet import IP, TCP
from scapy.all import *


def main():
    """
    Main function
    """
    p = Ether() / IP(dst="www.secdev.org") / TCP()
    print(p.summary())
    print(p.show())

    data = 'test_MACsec'

    pkt = Ether(dst="00:00:01:00:00:01",
                src="00:10:94:00:00:02") / MACsec() / data
    sendp(pkt, iface="en0", count=400)
    print(pkt.summary())
    print(pkt.show())


if __name__ == '__main__':
    main()
