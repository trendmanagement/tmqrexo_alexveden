import pickle
import pika
import logging
import sys
from pika.credentials import PlainCredentials
from datetime import datetime

RABBIT_EXCHANGE = "TMQR_SIGNALS"

from enum import Enum

APPCLASS_DATA = 'DataFeed'
APPCLASS_EXO = "ExoEngine"
APPCLASS_ALPHA = "AlphaStrategy"

class SignalApp(object):
    def __init__(self, appname, appclass, host='localhost', user='guest', password='guest'):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=host, credentials=PlainCredentials(user, password)))

        self.appname = appname
        self.appclass = appclass

        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=RABBIT_EXCHANGE, exchange_type='topic')

        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue

        self.channel.queue_bind(exchange=RABBIT_EXCHANGE,
                       queue=self.queue_name,
                       routing_key='{0}.{1}'.format(appclass, appname))


    def send(self, data):
        """
        Send data to default message ques appclass.appname
        :return:
        """
        self.channel.basic_publish(exchange=RABBIT_EXCHANGE,
                                   routing_key='{0}.{1}'.format(self.appclass, self.appname),
                                   body=pickle.dumps(data))

    def send_to(self, appname, appclass, data):
        """
        Send data to RabbitMQ message queue by routing key = appclass.appname
        :param appname: app name to notify, could be '*' to notify all apps
        :param appclass: root of routing key
        :param data: pickle friendly object
        :return:
        """
        self.channel.basic_publish(exchange=RABBIT_EXCHANGE,
                              routing_key='{0}.{1}'.format(appclass, appname),
                              body=pickle.dumps(data))

    def listen(self, callback):
        def pre_callback(ch, method, properties, body):
            if '.' not in method.routing_key:
                raise ValueError('Bad routing key format: {0}'.format(method.routing_key))

            tok = method.routing_key.split('.')
            if len(tok) != 2:
                raise ValueError('Bad routing key format: {0}'.format(method.routing_key))

            data_object = pickle.loads(body)
            callback(tok[0], tok[1], data_object)

        self.channel.basic_consume(pre_callback, queue=self.queue_name, no_ack=True)
        self.channel.start_consuming()

    def status(self, status, message, context={}):
        return {
            'type': 'status',
            'message': message,
            'status': status,
            'date': datetime.now(),
            'context': context,
            'appclass': self.appclass,
            'appname': self.appname,
        }
