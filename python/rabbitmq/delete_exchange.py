#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika

EXCHANGE_NAME = "ex.transfer.tst"

credentials = pika.PlainCredentials("user", "SP94Tea7TnRmHTea")

with pika.BlockingConnection(pika.ConnectionParameters(
        host="20.93.216.134", credentials=credentials)) as connection:
    channel = connection.channel()
    channel.exchange_delete(exchange=EXCHANGE_NAME)
    connection.close()
