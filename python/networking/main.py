#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from prometheus_client import Summary

import scapy.all as scapy
from scapy.layers.inet import Ether
from scapy.contrib.macsec import MACsec, MACsecSA
from scapy.layers.inet import IP, TCP
from scapy.data import ETH_P_MACSEC
from scapy.all import *


def main():
    """
    Main function
    """
    x = Ether() / IP(dst="www.secdev.org") / TCP()
    print(x.summary())
    print(x.show())

    data = 'test_MACsec'
    pkt = Ether(dst="00:00:01:00:00:01",
                src="00:10:94:00:00:02") / MACsec() / data
    sendp(pkt, iface="en0", count=400)
    print(pkt.summary())
    print(pkt.show())

    sa = MACsecSA(sci=b'\x52\x54\x00\x13\x01\x56\x00\x01', an=0, pn=100,
                  key=b'aaaaaaaaaaaaaaaa', icvlen=16, encrypt=1, send_sci=1)
    p = Ether(src='aa:aa:aa:bb:bb:bb', dst='cc:cc:cc:dd:dd:dd')/IP(src='192.168.0.1', dst='192.168.0.2')/ICMP(type='echo-request') / \
        "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
    m = sa.encap(p)
    print(m.type == ETH_P_MACSEC)
    print(m[MACsec].type == ETH_P_IP)
    print(len(m) == len(p) + 16)
    print(m[MACsec].an == 0)
    print(m[MACsec].pn == 100)
    print(m[MACsec].shortlen == 0)
    print(m[MACsec].SC)
    print(m[MACsec].E)
    print(m[MACsec].C)
    print(m[MACsec].sci == b'\x52\x54\x00\x13\x01\x56\x00\x01')
    print(p.show())


if __name__ == '__main__':
    main()
