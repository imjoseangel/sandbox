#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from rich import print as rprint

HEX = "c9980120000100000000000103777777076578616d706c6503636f6d00000100010000291000000000000000"

sock = socket.socket()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

x = sock.bind(('0.0.0.0', 12345))
y = sock.connect(('8.8.8.8', 53))

bytestream = bytes.fromhex(HEX)
rprint(f'Sent: {bytestream}')

sock.send(bytestream)

# get the reply
reply, _ = sock.recvfrom(1024)
rprint(f'Recv: {reply}')
