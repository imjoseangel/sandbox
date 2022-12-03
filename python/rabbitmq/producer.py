#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika

QUEUE_NAME = "mailbox"

credentials = pika.PlainCredentials('user', 'user')
with pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials)) as connection:
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    while True:
        message = input("Message: ")
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=message.encode("utf-8")
        )
