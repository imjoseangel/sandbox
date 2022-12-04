#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika

EXCHANGE_NAME = "ex.transfer.tst"
QUEUE_NAME = "qu.transfer.tst"

credentials = pika.PlainCredentials("user", "SP94Tea7TnRmHTea")

with pika.BlockingConnection(pika.ConnectionParameters(
        host="20.93.216.134", credentials=credentials)) as connection:
    try:
        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE_NAME,
                                 exchange_type="direct", durable=True)
        channel.queue_declare(queue=QUEUE_NAME, arguments={
            'x-message-ttl': 10800000,
            'x-dead-letter-exchange': 'dlx'
        }, durable=True)

        while True:
            message = input("Message: ")
            channel.basic_publish(
                exchange=EXCHANGE_NAME,
                routing_key=QUEUE_NAME,
                body=message.encode("utf-8")
            )
    except (KeyboardInterrupt, EOFError, pika.exceptions.StreamLostError):
        print("Exiting...")
        connection.close()
