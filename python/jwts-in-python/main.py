#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidAlgorithmError
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

new_token = jwt.encode(
    payload=payload_data,
    key=key,
    algorithm='RS256'
)

print(new_token)

print(jwt.decode(token, key='my_super_secret', algorithms=['HS256', ]))
print(jwt.get_unverified_header(token))

# saving the header claims into a variable
header_data = jwt.get_unverified_header(token)
# using that variable in the decode method
print(jwt.decode(
    token,
    key='my_super_secret',
    algorithms=[header_data['alg'], ]
))

public_key = open('/Users/imjoseangel/.ssh/id_rsa.pub',
                  'r', encoding='UTF-8').read()
key = serialization.load_ssh_public_key(public_key.encode())

print(jwt.decode(jwt=new_token, key=key, algorithms=['RS256', ]))

header_data = jwt.get_unverified_header(new_token)

try:
    payload = jwt.decode(
        token,
        key='my_super_secret',
        algorithms=[header_data['alg'], ]
    )
except (ExpiredSignatureError, InvalidAlgorithmError) as error:
    print(f'Unable to decode the token, error: {error}')
