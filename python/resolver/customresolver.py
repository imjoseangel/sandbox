#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import socket
from functools import wraps
import requests


# mock /etc/hosts
# lock it in multithreading or use multiprocessing if an endpoint
# is bound to multiple IPs frequently
etc_hosts = {}


# decorate python built-in resolver
def custom_resolver(builtin_resolver):
    """
    Custom resolver
    """

    @wraps(builtin_resolver)
    def wrapper(*args, **kwargs):
        try:
            return etc_hosts[args[:2]]
        except KeyError:
            # fall back to builtin_resolver for endpoints not in etc_hosts
            return builtin_resolver(*args, **kwargs)

    return wrapper


def _bind_ip(domain_name, port, ip_address):
    '''
    resolve (domain_name,port) to a given ip
    '''
    key = (domain_name, port)
    # (family, type, proto, canonname, sockaddr)

    value = (socket.AF_INET,
             socket.SOCK_STREAM, 6, '', (ip_address, port))
    etc_hosts[key] = [value]


def main():
    """
    Main function
    """

    # monkey patching
    socket.getaddrinfo = custom_resolver(socket.getaddrinfo)

    _bind_ip('www.example.com', 443, '216.58.215.174')

    # this sends requests to 216.58.215.174
    response = requests.get('https://www.example.com', verify=True)
    print(response.text)


if __name__ == '__main__':
    main()
