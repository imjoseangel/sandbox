#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jwt
from cryptography.hazmat.primitives import serialization

payload_data = {
    "sub": "4242",
    "name": "Jessica Temporal",
    "nickname": "Jess"
}

my_secret = 'my_super_secret'

token = jwt.encode(
    payload=payload_data,
    key=my_secret
)

print(token)

# read and load the key
private_key = open('/Users/imjoseangel/.ssh/id_rsa',
                   'r', encoding='UTF-8').read()
key = serialization.load_ssh_private_key(private_key.encode(), password=b'')

token_rsa = jwt.encode(
    payload=payload_data,
    key=my_secret
)

print(token_rsa)
