#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import socket
from twisted.names import client
from twisted.internet import reactor


def do_lookup(domain):
    """
    Lookup function
    """
    hosts = "example"
    resolver = client.createResolver(
        servers=None, resolvconf=None, hosts=hosts)
    name = resolver.getHostByName(domain)
    name.addBoth(lookup_done)


def lookup_done(result):
    """
    Lookup done
    """
    try:
        print(result.name)
        print(result)
        reactor.stop()
    except Exception as e:
        print(socket.getaddrinfo('google.com', 80)[0][-1][0])
        reactor.stop()


def main():
    """
    Main function
    """
    domain = b'google.coms'
    reactor.callLater(0, do_lookup, domain)
    reactor.run()


if __name__ == '__main__':
    main()
