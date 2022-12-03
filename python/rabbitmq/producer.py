#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika

QUEUE_NAME = "qu.transfer.tst"

credentials = pika.PlainCredentials('user', 'password')

with pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', credentials=credentials)) as connection:
    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)
        while True:
            message = input("Message: ")
            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=message.encode("utf-8")
            )
    except KeyboardInterrupt:
        print("Exiting...")
