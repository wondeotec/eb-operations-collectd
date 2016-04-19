#!/usr/bin/env python
import pika
import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("config/config-queue-checker.ini")

queue_name = Config.get('queue', 'name')
queue_password = Config.get('queue', 'password')
queue_virtual_host = Config.get('queue', 'virtual_host')
queue_host = Config.get('queue', 'host')
queue_user = Config.get('queue', 'user')
queue_port = int(Config.get('queue', 'port'))
interval = int(Config.get('librato', 'interval'))


def on_callback(msg):
    print msg

params = pika.ConnectionParameters(
        host=queue_host,
        virtual_host=queue_virtual_host,
        port=queue_port,
        credentials=pika.credentials.PlainCredentials(queue_user, queue_password)
)

# Open a connection to RabbitMQ on localhost using all default parameters
connection = pika.BlockingConnection(parameters=params)

# Open the channel
channel = connection.channel()

# Declare the queue
channel.queue_declare(
        queue=queue_name,
        exclusive=True,
        auto_delete=False,
        passive=True
    )

# Re-declare the queue with passive flag
res = channel.queue_declare(
        queue=queue_name,
        durable=True,
        exclusive=False,
        auto_delete=False,
        passive=True
    )

print 'PUTVAL \"%s/rabbitmq/gauge-status\" interval=%s N:%s' % (queue_host, interval, res.method.message_count)
