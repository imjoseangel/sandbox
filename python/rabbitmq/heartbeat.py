#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
from time import sleep
QUEUE_NAME = "qu.transfer.tst"

credentials = pika.PlainCredentials('user', 'password')


def main():
    params = pika.ConnectionParameters(host='localhost',
                                       credentials=credentials,
                                       heartbeat=600,
                                       blocked_connection_timeout=300)

    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.confirm_delivery()

        channel.queue_declare(queue=QUEUE_NAME,
                              arguments={
                                  'x-message-ttl': 10800000,
                                  'x-dead-letter-exchange': 'dlx'
                              },
                              durable=True)

        for item in range(100000):
            channel.basic_publish(exchange='',
                                  routing_key=QUEUE_NAME,
                                  body="abc",
                                  properties=pika.BasicProperties(content_type='text/plain',
                                                                  delivery_mode=pika.DeliveryMode.Transient))
            print('Message publish was confirmed')
            sleep(0.5)

    except (KeyboardInterrupt,
            EOFError,
            pika.exceptions.StreamLostError,
            pika.exceptions.IncompatibleProtocolError,
            pika.exceptions.ConnectionClosedByBroker,
            pika.exceptions.ConnectionWrongStateError):

        print('Message could not be confirmed')


if __name__ == '__main__':
    main()
