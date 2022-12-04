#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika


def callback(channel, method, properties, body):
    message = body.decode("utf-8")
    print(f"Got message: {message}")


QUEUE_NAME = "qu.transfer.tst"

credentials = pika.PlainCredentials("user", "SP94Tea7TnRmHTea")

with pika.BlockingConnection(pika.ConnectionParameters(
        host="20.93.216.134", credentials=credentials)) as connection:
    try:
        channel = connection.channel()
        channel.basic_consume(
            queue=QUEUE_NAME,
            auto_ack=True,
            on_message_callback=callback
        )
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Exiting...")
        connection.close()
