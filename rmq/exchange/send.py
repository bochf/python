#!/usr/bin/env python
import pika
import sys
import time

def main(host, msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel    = connection.channel()
    
    channel.exchange_declare(exchange='logs', type='fanout')

    # send message to exchange
    channel.basic_publish(exchange='logs', routing_key='', body=msg)
    print " [x] Sent %r" % msg

    # disconnect
    connection.close()

if __name__ == '__main__':
    main('localhost', ' '.join(sys.argv[1:]) or "info: Hello RMQ")
