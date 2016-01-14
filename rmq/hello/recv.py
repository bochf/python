#!/usr/bin/env python
import pika

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

print(' [*] Waiting for message. To exit press CTRL+C')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel    = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_consume(callback, queue='hello', no_ack=True)

channel.start_consuming()
