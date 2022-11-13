#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

sock = socket.socket()

x = sock.bind(('0.0.0.0', 12345))
y = sock.connect(('8.8.8.8', 53))

print(x, y)
