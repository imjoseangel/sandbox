#!/usr/bin/env python
# -*- coding: utf-8 -*-


ciphertext = bytes.fromhex('5e8d11e2250c69229d9b851be3be854cfec95721c46d')
flag = bytes.fromhex(
    '6b871bf560037d6a95d19a12fda4ca51eac85734d67e')

message = b"This is a test message"


def byte_xor(ba1, ba2):
    """ XOR two byte strings """
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


# Decode the cipher-text to a byte string and make the plaintext a byte string
key = byte_xor(ciphertext, message)
flag = byte_xor(flag, key)

print(flag)
