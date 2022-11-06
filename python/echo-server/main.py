#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import http.server
import os
import socketserver
from rich import print as rprint

PORT = int(os.getenv("PORT", "8080"))


def main():

    Handler = http.server.SimpleHTTPRequestHandler

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            rprint(f"Echo server listening on port {PORT}.\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
