#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
QUEUE_NAME = "qu.transfer.tst"

credentials = pika.PlainCredentials('user', 'password')


def main():
    params = pika.ConnectionParameters(host='localhost',
                                       credentials=credentials,
                                       heartbeat=600,
                                       blocked_connection_timeout=300)

    conn = pika.BlockingConnection(params)
    chann = conn.channel()
    chann.queue_declare(queue=QUEUE_NAME, arguments={
        'x-message-ttl': 10800000,
        'x-dead-letter-exchange': 'dlx'
    }, durable=True)

    chann.basic_publish('', QUEUE_NAME, "abc")
    conn.close()


if __name__ == '__main__':
    main()
