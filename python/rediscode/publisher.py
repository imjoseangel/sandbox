#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis

with redis.Redis() as client:
    while True:
        message = input("Message: ")
        client.publish("chatroom", message)
