import pickle
import pika
import logging
import sys
from pika.credentials import PlainCredentials
from datetime import datetime
from tradingcore.messages import MsgBase
import json
from bson import json_util

RABBIT_EXCHANGE = "TMQR_SIGNALS"

from enum import Enum

APPCLASS_DATA = 'DataFeed'
APPCLASS_EXO = "ExoEngine"
APPCLASS_ALPHA = "AlphaStrategy"
APPCLASS_SIGNALS = "Signals"
APPCLASS_UTILS  = 'Utils'

import logging
import pika

from pika.connection import LOGGER as pika_logger

class LoggerFilterNormalCloseIsFine (logging.Filter):
    def filter(self, record):
        return not record.getMessage().endswith('(200): Normal shutdown')
pika_logger.addFilter(LoggerFilterNormalCloseIsFine())

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class SignalApp(object):
    def __init__(self, appname, appclass, host='localhost', user='guest', password='guest'):
        """Create a new instance of the consumer class, passing in the AMQP
        URL used to connect to RabbitMQ.

        """

        self._conn_params = pika.ConnectionParameters(
            host=host,
            credentials=PlainCredentials(user, password),
            heartbeat_interval=60)

        self.appname = appname
        self.appclass = appclass

        self.listen_callback = None

        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None

    def connect(self):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.

        :rtype: pika.SelectConnection
        """
        LOGGER.info('Connecting to RabbitMQ host')
        return pika.SelectConnection(self._conn_params,
                                     self.on_connection_open,
                                     stop_ioloop_on_close=False)

    def on_connection_open(self, unused_connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :type unused_connection: pika.SelectConnection

        """
        LOGGER.info('Connection opened')
        self.add_on_connection_close_callback()
        self.open_channel()

    def add_on_connection_close_callback(self):
        """This method adds an on close callback that will be invoked by pika
        when RabbitMQ closes the connection to the publisher unexpectedly.

        """
        LOGGER.info('Adding connection close callback')
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param int reply_code: The server provided reply_code if given
        :param str reply_text: The server provided reply_text if given

        """
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            LOGGER.warning('Connection closed, reopening in 5 seconds: (%s) %s',
                           reply_code, reply_text)
            self._connection.add_timeout(5, self.reconnect)

    def reconnect(self):
        """Will be invoked by the IOLoop timer if the connection is
        closed. See the on_connection_closed method.

        """
        # This is the old connection IOLoop instance, stop its ioloop
        self._connection.ioloop.stop()

        if not self._closing:
            # Create a new connection
            self._connection = self.connect()

            # There is now a new connection, needs a new ioloop to run
            self._connection.ioloop.start()

    def open_channel(self):
        """Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.

        """
        LOGGER.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.

        :param pika.channel.Channel channel: The channel object

        """
        LOGGER.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(RABBIT_EXCHANGE)

    def add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.

        """
        LOGGER.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel: The closed channel
        :param int reply_code: The numeric reason the channel was closed
        :param str reply_text: The text reason the channel was closed

        """
        LOGGER.warning('Channel %i was closed: (%s) %s',
                       channel, reply_code, reply_text)
        self._connection.close()

    def setup_exchange(self, exchange_name):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.

        :param str|unicode exchange_name: The name of the exchange to declare

        """
        LOGGER.info('Declaring exchange %s', exchange_name)
        self._channel.exchange_declare(self.on_exchange_declareok,
                                       exchange_name,
                                       exchange_type='topic')

    def on_exchange_declareok(self, unused_frame):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame

        """
        LOGGER.info('Exchange declared')

        self.setup_queue()

    def setup_queue(self):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.

        """
        LOGGER.info('Declaring queue')
        self._channel.queue_declare(self.on_queue_declareok) # queue_name='' for autonaming

    def on_queue_declareok(self, method_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """
        self.queue_name = method_frame.method.queue
        LOGGER.info('Binding %s to %s with %s',
                    RABBIT_EXCHANGE, self.queue_name, '{0}.{1}'.format(self.appclass, self.appname))
        self._channel.queue_bind(self.on_bindok, exchange=RABBIT_EXCHANGE,
                       queue=self.queue_name, routing_key='{0}.{1}'.format(self.appclass, self.appname))

    def on_bindok(self, unused_frame):
        """Invoked by pika when the Queue.Bind method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.

        :param pika.frame.Method unused_frame: The Queue.BindOk response frame

        """
        LOGGER.info('Queue bound')
        self.start_consuming()

    def start_consuming(self):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.

        """
        LOGGER.info('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.on_message,
                                                         self.queue_name)

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """
        LOGGER.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        LOGGER.info('Consumer was cancelled remotely, shutting down: %r',
                    method_frame)
        if self._channel:
            self._channel.close()



    def acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """
        LOGGER.info('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.

        """
        if self._channel:
            LOGGER.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            self._channel.basic_cancel(self.on_cancelok, self._consumer_tag)

    def on_cancelok(self, unused_frame):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        :param pika.frame.Method unused_frame: The Basic.CancelOk frame

        """
        LOGGER.info('RabbitMQ acknowledged the cancellation of the consumer')
        self.close_channel()

    def close_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.

        """
        LOGGER.info('Closing the channel')
        self._channel.close()


    def stop(self):
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.

        """
        LOGGER.info('Stopping')
        self._closing = True
        self.stop_consuming()
        self._connection.ioloop.stop()
        LOGGER.info('Stopped')

    def close_connection(self):
        """This method closes the connection to RabbitMQ."""
        LOGGER.info('Closing connection')
        self._connection.close()

    def send(self, data):
        """
        Send data to default message ques appclass.appname
        :return:
        """
        return self.send_to(self.appname, self.appclass, data)

    def send_to(self, appname, appclass, data):
        """
        Send data to RabbitMQ message queue by routing key = appclass.appname
        :param appname: app name to notify, could be '*' to notify all apps
        :param appclass: root of routing key
        :param data: pickle friendly object
        :return:
        """
        connection = pika.BlockingConnection(self._conn_params)
        channel = connection.channel()
        channel.exchange_declare(exchange=RABBIT_EXCHANGE, exchange_type='topic')

        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=RABBIT_EXCHANGE,
                           queue=queue_name,
                           routing_key='{0}.{1}'.format(appclass, appname))

        if isinstance(data, MsgBase):
            data.sender_appname = appname
            data.sender_appclass = appclass
            channel.basic_publish(exchange=RABBIT_EXCHANGE,
                                  routing_key='{0}.{1}'.format(appclass, appname),
                                  body=pickle.dumps(data.as_dict()))
        else:
            channel.basic_publish(exchange=RABBIT_EXCHANGE,
                                  routing_key='{0}.{1}'.format(appclass, appname),
                                  body=pickle.dumps(data))
        connection.close()

    def listen(self, callback):
        """Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.

        """
        self.listen_callback = callback
        self._connection = self.connect()
        self._connection.ioloop.start()

    def on_message(self, unused_channel, method, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body

        """

        try:
            LOGGER.info('Received message # %s from %s: %s',
                        method.delivery_tag, properties.app_id, body)

            if '.' not in method.routing_key:
                LOGGER.error('Bad routing key format: {0}'.format(method.routing_key))
                self.acknowledge_message(method.delivery_tag)
                return

            tok = method.routing_key.split('.')
            if len(tok) != 2:
                LOGGER.error('Bad routing key format: {0}'.format(method.routing_key))
                self.acknowledge_message(method.delivery_tag)
                return

            appclass = tok[0]
            appname = tok[1]

            try:
                # This is pickled dictionary
                data_object = MsgBase(pickle.loads(body))
            except TypeError:
                try:
                    data_object = MsgBase(json.loads(body, object_hook=json_util.object_hook))
                except:
                    LOGGER.error('Failed to load JSON from {0}'.format(body))
                    self.acknowledge_message(method.delivery_tag)
                    return

            if self.listen_callback is not None:
                self.listen_callback(appclass, appname, data_object)
        except Exception as exc:
            LOGGER.error('Exception occurred {0}'.format(exc))
            raise exc
        finally:
            self.acknowledge_message(method.delivery_tag)





