#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika

QUEUE_NAME = "qu.transfer.tst"

credentials = pika.PlainCredentials("user", "password")

with pika.BlockingConnection(pika.ConnectionParameters(
        host="localhost", credentials=credentials)) as connection:
    channel = connection.channel()
    channel.queue_delete(queue=QUEUE_NAME)
    connection.close()
