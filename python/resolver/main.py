#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import requests
from requests_toolbelt.adapters import host_header_ssl


def main():
    """
    Main function
    """
    request_session = requests.Session()
    request_session.mount('https://', host_header_ssl.HostHeaderSSLAdapter())

    response = request_session.get(
        'https://1.2.3.4', headers={'Host': 'example.com'}, verify=True)

    print(response.text)


if __name__ == '__main__':
    main()
