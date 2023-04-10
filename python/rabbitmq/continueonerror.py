#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import pika

QUEUE_NAME = "qu.transfer.tst"

credentials = pika.PlainCredentials('user', 'password')

while (True):
    try:
        print("Connecting...")
        # Shuffle the hosts list before reconnecting.
        # This can help balance connections.

        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost', credentials=credentials))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        # This queue is intentionally non-durable. See http://www.rabbitmq.com/ha.html#non-mirrored-queue-behavior-on-node-failure
        # to learn more.
        channel.queue_declare(queue=QUEUE_NAME, arguments={
            'x-message-ttl': 10800000,
            'x-dead-letter-exchange': 'dlx'
        }, durable=True)
        try:
            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body="test"
            )
            sleep(1)
        except KeyboardInterrupt:
            channel.stop_consuming()
            connection.close()
            break
    except pika.exceptions.ConnectionClosedByBroker:
        # Uncomment this to make the example not attempt recovery
        # from server-initiated connection closure, including
        # when the node is stopped cleanly
        #
        # break
        continue
    # Do not recover on channel errors
    except pika.exceptions.AMQPChannelError as err:
        print("Caught a channel error: {}, stopping...".format(err))
        break
    # Recover on all other connection errors
    except pika.exceptions.AMQPConnectionError:
        print("Connection was closed, retrying...")
        continue
