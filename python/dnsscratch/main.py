#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Big Julia: https://jvns.ca/blog/2022/11/06/making-a-dns-query-in-ruby-from-scratch/

import random
import socket
from rich import print as rprint

HEX = "b96201000001000000000000076578616d706c6503636f6d0000010001"


def make_question_header(query_id):
    """
    :param query_id:
    :return header:
    """
    # id, flags, num questions, num answers, num auth, num additional
    header = ['\x01\x00', '\x00\x01',
              '\x00\x00', '\x00\x00', '\x00\x00']
    return query_id + ''.join(header).encode()


def encode_domain_name(domain):
    """
    :param domain:
    :return:
    """
    parts = domain.split('.')
    parts = list(map(lambda s: chr(len(s)) + s, parts))

    return ''.join(parts).encode()


def make_dns_query(domain, dnstype):
    query_id = bytes.fromhex(f'{random.randint(0, 65535):04x}')
    header = make_question_header(query_id)
    question = encode_domain_name(domain)
    tail = ['\x00', chr(dnstype), '\x01\x00\x01']

    return header + question + ''.join(tail).encode()


sock = socket.socket()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

x = sock.bind(('0.0.0.0', 12345))
y = sock.connect(('8.8.8.8', 53))

bytestream = make_dns_query('example.com', 1)
rprint(f'Sent: {bytestream}')

sock.send(bytestream)

# get the reply
reply, _ = sock.recvfrom(1024 * 4)
rprint(f'Recv: {reply}')
