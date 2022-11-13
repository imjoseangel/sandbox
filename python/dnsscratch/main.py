#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import socket
from rich import print as rprint

HEX = "c9980120000100000000000103777777076578616d706c6503636f6d00000100010000291000000000000000"


def make_question_header(query_id):
    """
    :param query_id:
    :return header:
    """
    # id, flags, num questions, num answers, num auth, num additional
    header = [query_id, 0x0120, 0x0001, 0x0000, 0x0000, 0x0001]
    return ''.join([f'{field:04x}' for field in header])


def encode_domain_name(domain):
    """
    :param domain:
    :return:
    """
    parts = domain.split('.')
    parts = list(map(lambda s: chr(len(s)) + s, parts))

    return ''.join(parts).encode()


def make_dns_query(domain):
    query_id = random.randint(0, 65535)
    header = make_question_header(query_id)


print(make_question_header(0xc998))
print(encode_domain_name('example.com'))


# sock = socket.socket()
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# x = sock.bind(('0.0.0.0', 12345))
# y = sock.connect(('8.8.8.8', 53))

# bytestream = bytes.fromhex(HEX)
# rprint(f'Sent: {bytestream}')

# sock.send(bytestream)

# # get the reply
# reply, _ = sock.recvfrom(1024)
# rprint(f'Recv: {reply}')
