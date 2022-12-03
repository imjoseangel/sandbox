#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika

QUEUE_NAME = "qu.transfer.tst"

credentials = pika.PlainCredentials('user', 'password')


def callback(channel, method, properties, body):
    message = body.decode("utf-8")
    print(f"Got message: {message}")


with pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', credentials=credentials)) as connection:
    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)
        channel.basic_consume(
            queue=QUEUE_NAME,
            auto_ack=True,
            on_message_callback=callback
        )
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Exiting...")
