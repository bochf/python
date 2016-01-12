#!/usr/bin/env python
import pika
import sys

def main(host, msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel    = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(exchange='', routing_key='task_queue', body=msg, properties=pika.BasicProperties(delivery_mode=2))

    print(" [x] Sent %r" % msg)

    connection.close()

if __name__ == "__main__":
    message = ' '.join(sys.argv[1:]) or "Hello RMQ"
    main('localhost', message)
