#!/usr/bin/env python
import pika

def main(host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    for i in range(0, 1000):
        msg = 'Hello RMQ ' + `i`
        channel.basic_publish(exchange='', routing_key='hello', body=msg)
        print (" [x] Sent '{}'".format(msg))

    connection.close()

if __name__ == "__main__":
    main('localhost')
