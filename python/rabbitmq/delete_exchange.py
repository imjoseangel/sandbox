#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika

EXCHANGE_NAME = "ex.transfer.tst"

credentials = pika.PlainCredentials("user", "password")

with pika.BlockingConnection(pika.ConnectionParameters(
        host="localhost", credentials=credentials)) as connection:
    channel = connection.channel()
    channel.exchange_delete(exchange=EXCHANGE_NAME)
    connection.close()
