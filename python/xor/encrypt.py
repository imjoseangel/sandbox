#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from Crypto.Cipher import ChaCha20


FLAG = b'abcdefghijklmnopqrstuv'


def encryptMessage(message, key, nonce):
    cipher = ChaCha20.new(key=key, nonce=nonce)
    ciphertext = cipher.encrypt(message)
    return ciphertext


if __name__ == "__main__":

    plaintext = b"This is a test message"

    iv = bytes.fromhex('c4a66edfe80227b4fa24d431')
    mykey = os.urandom(32)

    encrypted_message = encryptMessage(plaintext, mykey, iv)
    encrypted_flag = encryptMessage(FLAG, mykey, iv)

    data = encrypted_message.hex() + "\n" + encrypted_flag.hex()

    print(data)
