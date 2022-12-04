#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika

EXCHANGE_NAME = "ex.transfer.tst"

credentials = pika.PlainCredentials("user", "SP94Tea7TnRmHTea")

with pika.BlockingConnection(pika.ConnectionParameters(
        host="20.93.216.134", credentials=credentials)) as connection:
    try:
        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE_NAME,
                                 exchange_type="fanout", durable=True)

        while True:
            message = input("Message: ")
            channel.basic_publish(
                exchange=EXCHANGE_NAME,
                routing_key="",
                body=message.encode("utf-8")
            )
    except (KeyboardInterrupt, EOFError, pika.exceptions.StreamLostError):
        print("Exiting...")
        connection.close()
