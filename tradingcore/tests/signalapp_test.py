import unittest
from unittest.mock import Mock, MagicMock, patch
from tradingcore.signalapp import SignalApp
from tradingcore.messages import MsgStatus
import pickle
import json
from bson import json_util


class SignalAppTestCase(unittest.TestCase):
    def test_init(self):
        app = SignalApp('test_app', 'test_class')
        self.assertEqual(app.appname, 'test_app')
        self.assertEqual(app.appclass, 'test_class')

    def test_on_message_valid_pickle_data(self):
        app = SignalApp('test_app', 'test_class')

        app._channel = MagicMock(spec='pika.channel.Channel')
        app._channel.basic_ack = Mock()

        method = MagicMock(spec='pika.Spec.Basic.Deliver')
        method.delivery_tag = 'tag'
        method.routing_key = 'test_class.test_app'

        properties = MagicMock(spec='pika.Spec.BasicProperties')
        properties.app_id = 'appid'

        callback = Mock()

        msg_data = pickle.dumps({'test': 'message'})

        app.listen_callback = callback
        app.on_message('channel', method, properties, msg_data)

        self.assertEqual(True, app._channel.basic_ack.called)
        self.assertEqual(True, callback.called)
        self.assertEqual(('test_class', 'test_app', {'test': 'message'}), callback.call_args[0])

    def test_on_message_valid_pickle_empty_routing_key(self):
        app = SignalApp('test_app', 'test_class')

        app._channel = MagicMock(spec='pika.channel.Channel')
        app._channel.basic_ack = Mock()

        method = MagicMock(spec='pika.Spec.Basic.Deliver')
        method.delivery_tag = 'tag'
        method.routing_key = ''

        properties = MagicMock(spec='pika.Spec.BasicProperties')
        properties.app_id = 'appid'

        callback = Mock()

        msg_data = pickle.dumps({'test': 'message'})

        app.listen_callback = callback
        app.on_message('channel', method, properties, msg_data)

        self.assertEqual(True, app._channel.basic_ack.called)
        self.assertEqual(False, callback.called)

    def test_on_message_valid_pickle_invalid_routing_key(self):
        app = SignalApp('test_app', 'test_class')

        app._channel = MagicMock(spec='pika.channel.Channel')
        app._channel.basic_ack = Mock()

        method = MagicMock(spec='pika.Spec.Basic.Deliver')
        method.delivery_tag = 'tag'
        method.routing_key = ''

        properties = MagicMock(spec='pika.Spec.BasicProperties')
        properties.app_id = 'appid'

        callback = Mock()

        msg_data = pickle.dumps({'test': 'message'})

        app.listen_callback = callback
        app.on_message('channel', method, properties, msg_data)

        self.assertEqual(True, app._channel.basic_ack.called)
        self.assertEqual(False, callback.called)

    def test_on_message_valid_pickle_invalid_dataformat(self):
        app = SignalApp('test_app', 'test_class')

        app._channel = MagicMock(spec='pika.channel.Channel')
        app._channel.basic_ack = Mock()

        method = MagicMock(spec='pika.Spec.Basic.Deliver')
        method.delivery_tag = 'tag'
        method.routing_key = 'test_app.test_class'

        properties = MagicMock(spec='pika.Spec.BasicProperties')
        properties.app_id = 'appid'

        callback = Mock()

        msg_data = 'simple text data'

        app.listen_callback = callback
        app.on_message('channel', method, properties, msg_data)

        self.assertEqual(True, app._channel.basic_ack.called)
        self.assertEqual(False, callback.called)

    def test_on_message_valid_pickle_json_format(self):
        app = SignalApp('test_app', 'test_class')

        app._channel = MagicMock(spec='pika.channel.Channel')
        app._channel.basic_ack = Mock()

        method = MagicMock(spec='pika.Spec.Basic.Deliver')
        method.delivery_tag = 'tag'
        method.routing_key = 'test_app.test_class'

        properties = MagicMock(spec='pika.Spec.BasicProperties')
        properties.app_id = 'appid'

        callback = Mock()

        msg_data = json.dumps(MsgStatus('text', 'test status', notify=True).as_dict(), default=json_util.default)

        app.listen_callback = callback
        app.on_message('channel', method, properties, msg_data)

        self.assertEqual(True, app._channel.basic_ack.called)
        self.assertEqual(True, callback.called)



if __name__ == '__main__':
    unittest.main()

