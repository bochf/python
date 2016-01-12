#!/usr/bin/env python
import pika
import sys
import time

def callback(ch, method, properties, body):
    print " [x] %r" % body

def listen(host):
    print " [*] Waiting for messages. To exit press CTRL+C"

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel    = connection.channel()

    qName = channel.queue_declare(exclusive=True).method.queue
    channel.exchange_declare(exchange='logs', type='fanout')
    channel.queue_bind(exchange='logs', queue=qName)

    channel.basic_consume(callback, queue=qName, no_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    listen('localhost')

