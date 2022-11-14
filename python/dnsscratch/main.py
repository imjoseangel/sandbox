#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Big Julia: https://jvns.ca/blog/2022/11/06/making-a-dns-query-in-ruby-from-scratch/
# Another ref: https://stackoverflow.com/questions/34793061/socket-resolve-dns-with-specific-dns-server

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
    header = [query_id, '\x01\x20', '\x00\x01',
              '\x00\x00', '\x00\x00', '\x00\x01']
    return ''.join([field for field in header]).encode().hex()


def encode_domain_name(domain):
    """
    :param domain:
    :return:
    """
    parts = domain.split('.')
    parts = list(map(lambda s: chr(len(s)) + s, parts))

    return ''.join(parts).encode().hex()


def make_dns_query(domain):
    query_id = random.randint(0, 65535)
    header = make_question_header(hex(query_id))
    question = encode_domain_name(domain)

    return header + question


print(make_question_header('\xc9\x98'))
print(encode_domain_name('www.example.com'))
print(make_dns_query('www.example.com'))

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
