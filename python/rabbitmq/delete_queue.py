#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika

QUEUE_NAME = "qu.transfer.tst"

credentials = pika.PlainCredentials("user", "SP94Tea7TnRmHTea")

with pika.BlockingConnection(pika.ConnectionParameters(
        host="20.93.216.134", credentials=credentials)) as connection:
    channel = connection.channel()
    channel.queue_delete(queue=QUEUE_NAME)
    connection.close()
