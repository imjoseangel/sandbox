#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base64 import b64encode, b64decode


def asciiChar2Value(a):
    b = '.'.join(str(ord(c)) for c in a)
    print(b)
    return b


def Value2asciiChar(a):
    b = '.'.join(str(chr(c)) for c in a)
    print(b)


def reverse(a):
    return a[::-1]


def encrypt_to_ip(a, iterations):
    # print(iterations)
    for i in range(iterations):
        # print (i)
        if i % 2 == 0:
            a = b64encode(a.encode()).decode()
            # print(a)
        else:
            a = reverse(a)
        print(a)
    b = asciiChar2Value(a)
    l = []
    ips = []
    count = 1
    for i in b.split('.'):
        l.append(i)
        if count % 4 == 0:
            conc = '.'.join(j for j in l)
            ips.append(conc)
            l = []
        count = count + 1

    if len(l) != 0:
        ips.append('.'.join(j for j in l))

    return ips


def decrypt_to_ip(a, iterations):
    for i in range(iterations):
        if i % 2 == 0:
            a = b64decode(a.encode()).decode()


plaintext = 'ctfhw9{blablabla}'

encrypted = encrypt_to_ip(plaintext, 7)

for ip in encrypted:
    print(ip)
