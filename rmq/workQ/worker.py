#!/usr/bin/env python
import pika
import time
import thread

def processMsg(body):
    print(" [x] Start processing message %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Process message %r done" % body)

def sync_worker(ch, method, properties, body):
    processMsg(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def async_worker(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    try:
        thread.start_new_thread(processMsg, (body,))
    except:
        print "Error: unable to start worker thread"

def listen(host, async):
    print " [*] Waiting for messages. To exit press CTRL+C"

    connection = pika.BlockingConnection(pika.ConnectionParameters(host))
    channel    = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_qos(prefetch_count=1)
    if (async):
        channel.basic_consume(async_worker, queue='task_queue')
    else:
        channel.basic_consume(sync_worker, queue='task_queue')

    channel.start_consuming()

if __name__ == '__main__':
    listen('localhost', False)
