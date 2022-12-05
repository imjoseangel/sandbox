#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika

EXCHANGE_NAME = "ex.transfer.tst"
QUEUE_NAME = "qu.transfer.tst"


def callback(channel, method, properties, body):
    message = body.decode("utf-8")
    print(f"Got message: {message}")


credentials = pika.PlainCredentials("user", "password")

with pika.BlockingConnection(pika.ConnectionParameters(
        host="localhost", credentials=credentials)) as connection:
    try:
        channel = connection.channel()

        channel.queue_bind(exchange=EXCHANGE_NAME,
                           queue=QUEUE_NAME, routing_key=QUEUE_NAME)

        channel.basic_consume(
            queue=QUEUE_NAME,
            auto_ack=True,
            on_message_callback=callback
        )
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Exiting...")
        connection.close()
