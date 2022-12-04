#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika

EXCHANGE_NAME = "ex.transfer.tst"


def callback(channel, method, properties, body):
    message = body.decode("utf-8")
    print(f"Got message: {message}")


credentials = pika.PlainCredentials("user", "SP94Tea7TnRmHTea")

with pika.BlockingConnection(pika.ConnectionParameters(
        host="20.93.216.134", credentials=credentials)) as connection:
    try:
        channel = connection.channel()

        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

        channel.basic_consume(
            queue=queue_name,
            auto_ack=True,
            on_message_callback=callback
        )
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Exiting...")
        connection.close()
