#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jwt


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
