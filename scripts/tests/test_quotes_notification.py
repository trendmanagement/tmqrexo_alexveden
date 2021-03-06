import logging
import pprint
import unittest
from unittest.mock import Mock, patch

from pymongo import MongoClient

from scripts.quotes_notification import QuotesNotifyScript, STATUS_QUOTES_COLLECTION
from scripts.settings import *
from scripts.settings_local import *
from tradingcore.messages import *
from tradingcore.signalapp import SignalApp
import datetime

class QuotesNotificationTestCase(unittest.TestCase):
    def test_init(self):
        qn = QuotesNotifyScript(None, logging.DEBUG)

        self.assertEqual(qn.args, None)
        self.assertEqual(qn.asset_info, None)
        self.assertEqual(qn.loglevel, logging.DEBUG)
        self.assertEqual(qn.last_quote_date, None)
        self.assertEqual(qn.last_minute, -1)
        self.assertEqual(type(qn.pprinter), pprint.PrettyPrinter)

    @patch('exobuilder.data.assetindex_mongo.AssetIndexMongo.get_exec_time')
    def test_process_quote(self, mock_get_exec_time):
        with patch('tradingcore.signalapp.SignalApp', spec=SignalApp) as mock_signalapp,  \
                patch('scripts.quotes_notification.QuotesNotifyScript.date_now') as mock_now, \
                patch('scripts.quotes_notification.QuotesNotifyScript.get_last_quote_date') as mock_get_last_quote_date, \
                patch('scripts.quotes_notification.QuotesNotifyScript.set_last_quote_state') as mock_set_last_quote_date:

            mock_args = Mock()
            mock_args.instrument = 'TEST'

            qn = QuotesNotifyScript(mock_args, logging.DEBUG)
            last_bt = datetime.datetime(2016, 1, 1, 13, 46, 00)

            mock_now.return_value = datetime.datetime(2016, 1, 1, 13, 45, 00)
            # exec_time, decision_time
            mock_get_exec_time.return_value = datetime.datetime(2016, 1, 1, 13, 45, 00), datetime.datetime(2016, 1, 1, 13, 40, 00)

            mock_get_last_quote_date.return_value = datetime.datetime(2015, 1, 1, 13, 45, 00)

            qn.signalapp = mock_signalapp
            qn.process_quote(last_bt)

            self.assertEqual(True, mock_signalapp.send.called)
            self.assertEqual(2, mock_signalapp.send.call_count)

            self.assertEqual(mock_signalapp.send.call_args_list[0][0][0].mtype, 'status')
            self.assertEqual(mock_signalapp.send.call_args_list[0][0][0].status, 'RUN')

            msg = mock_signalapp.send.call_args_list[1][0][0]
            self.assertEqual(msg.mtype, 'quote')

            self.assertEqual(msg.context['decision_time'], mock_get_exec_time.return_value[1])
            self.assertEqual(msg.context['execution_time'], mock_get_exec_time.return_value[0])
            self.assertEqual(msg.context['instrument'], mock_args.instrument)
            self.assertEqual(msg.context['last_bar_time'], last_bt)
            self.assertEqual(msg.context['last_run_date'], last_bt)
            self.assertEqual(msg.context['now'], mock_now.return_value)



    def test_process_quote_first_run_same_date(self):
        with patch('tradingcore.signalapp.SignalApp', spec=SignalApp) as mock_signalapp,  \
                patch('scripts.quotes_notification.QuotesNotifyScript.date_now') as mock_now, \
                patch('scripts.quotes_notification.QuotesNotifyScript.get_last_quote_date') as mock_get_last_quote_date, \
                patch('scripts.quotes_notification.QuotesNotifyScript.set_last_quote_state') as mock_set_last_quote_date, \
                patch('exobuilder.data.assetindex_mongo.AssetIndexMongo.get_exec_time') as mock_get_exec_time:

            mock_args = Mock()
            mock_args.instrument = 'TEST'

            qn = QuotesNotifyScript(mock_args, logging.DEBUG)
            last_bt = datetime.datetime(2016, 1, 1, 13, 46, 00)

            mock_get_last_quote_date.return_value = datetime.datetime(2016, 1, 1, 13, 45, 00)
            mock_now.return_value = datetime.datetime(2016, 1, 1, 13, 45, 00)

            # exec_time, decision_time
            mock_get_exec_time.return_value = datetime.datetime(2016, 1, 1, 13, 45, 00), datetime.datetime(2016, 1, 1, 13, 40, 00)

            qn.signalapp = mock_signalapp
            qn.process_quote(last_bt)

            self.assertEqual(True, mock_signalapp.send.called)
            self.assertEqual(mock_signalapp.send.call_args_list[0][0][0].mtype, 'status')
            self.assertEqual(mock_signalapp.send.call_args_list[0][0][0].status, 'IDLE')

    def test_process_quote_first_run_same_before_decision_time(self):
        with patch('tradingcore.signalapp.SignalApp', spec=SignalApp) as mock_signalapp, \
                patch('scripts.quotes_notification.QuotesNotifyScript.date_now') as mock_now, \
                patch(
                    'scripts.quotes_notification.QuotesNotifyScript.get_last_quote_date') as mock_get_last_quote_date, \
                patch(
                    'scripts.quotes_notification.QuotesNotifyScript.set_last_quote_state') as mock_set_last_quote_date, \
                patch('exobuilder.data.assetindex_mongo.AssetIndexMongo.get_exec_time') as mock_get_exec_time:
            mock_args = Mock()
            mock_args.instrument = 'TEST'

            qn = QuotesNotifyScript(mock_args, logging.DEBUG)
            last_bt = datetime.datetime(2016, 1, 1, 13, 45, 00)

            mock_get_last_quote_date.return_value = datetime.datetime(2016, 1, 1, 13, 45, 00)
            mock_now.return_value = datetime.datetime(2016, 1, 1, 13, 45, 00)

            # exec_time, decision_time
            mock_get_exec_time.return_value = datetime.datetime(2016, 1, 1, 13, 45, 00), datetime.datetime(2016, 1,
                                                                                                           1, 13,
                                                                                                           40, 00)
            qn.last_quote_date = datetime.datetime(2016, 1, 1, 12, 46, 00)
            qn.signalapp = mock_signalapp
            qn.process_quote(last_bt)

            self.assertEqual(True, mock_signalapp.send.called)
            self.assertEqual(mock_signalapp.send.call_args_list[0][0][0].mtype, 'status')
            self.assertEqual(mock_signalapp.send.call_args_list[0][0][0].status, 'IDLE')

    def test_check_quote_delay_with_idle(self):
        with patch('tradingcore.signalapp.SignalApp', spec=SignalApp) as mock_signalapp, \
                patch('scripts.quotes_notification.QuotesNotifyScript.date_now') as mock_now, \
                patch('scripts.quotes_notification.QuotesNotifyScript.get_last_quote_date') as mock_get_last_quote_date, \
                patch('scripts.quotes_notification.QuotesNotifyScript.set_last_quote_state') as mock_set_last_quote_date, \
                patch('exobuilder.data.assetindex_mongo.AssetIndexMongo.get_exec_time') as mock_get_exec_time:
            mock_args = Mock()
            mock_args.instrument = 'TEST'
            mock_args.delay = 3

            qn = QuotesNotifyScript(mock_args, logging.DEBUG)

            last_bt = datetime.datetime(2016, 2, 1, 12, 40, 00)

            mock_get_last_quote_date.return_value = datetime.datetime(2015, 2, 1, 12, 45, 00)
            mock_now.return_value = datetime.datetime(2016, 2, 1, 12, 45, 00)

            # exec_time, decision_time
            mock_get_exec_time.return_value = datetime.datetime(2016, 2, 1, 12, 45, 00), datetime.datetime(2016, 2,
                                                                                                           1, 12,
                                                                                                           40, 00)
            qn.last_quote_date = datetime.datetime(2016, 2, 1, 11, 46, 00)
            qn.signalapp = mock_signalapp
            qn.process_quote(last_bt)

            self.assertEqual(True, mock_signalapp.send.called)
            self.assertEqual(mock_signalapp.send.call_args_list[0][0][0].mtype, 'status')
            self.assertEqual(mock_signalapp.send.call_args_list[0][0][0].status, 'DELAY')

            self.assertEqual(mock_signalapp.send.call_args_list[1][0][0].mtype, 'status')
            self.assertEqual(mock_signalapp.send.call_args_list[1][0][0].status, 'IDLE')

    def test_check_quote_delay_with_run(self):
        with patch('tradingcore.signalapp.SignalApp', spec=SignalApp) as mock_signalapp, \
                patch('scripts.quotes_notification.QuotesNotifyScript.date_now') as mock_now, \
                patch('scripts.quotes_notification.QuotesNotifyScript.get_last_quote_date') as mock_get_last_quote_date, \
                patch('scripts.quotes_notification.QuotesNotifyScript.set_last_quote_state') as mock_set_last_quote_date, \
                patch('exobuilder.data.assetindex_mongo.AssetIndexMongo.get_exec_time') as mock_get_exec_time:
            mock_args = Mock()
            mock_args.instrument = 'TEST'
            mock_args.delay = 3

            qn = QuotesNotifyScript(mock_args, logging.DEBUG)

            last_bt = datetime.datetime(2016, 2, 1, 12, 47, 00)

            mock_get_last_quote_date.return_value = datetime.datetime(2015, 1, 1, 12, 45, 00)
            mock_now.return_value = datetime.datetime(2016, 2, 1, 12, 56, 00)

            # exec_time, decision_time
            mock_get_exec_time.return_value = datetime.datetime(2016, 2, 1, 12, 45, 00), datetime.datetime(2016, 2,
                                                                                                           1, 12,
                                                                                                           40, 00)
            qn.last_quote_date = datetime.datetime(2016, 1, 1, 11, 46, 00)
            qn.signalapp = mock_signalapp
            qn.process_quote(last_bt)

            self.assertEqual(True, mock_signalapp.send.called)
            self.assertEqual(mock_signalapp.send.call_args_list[0][0][0].mtype, 'status')
            self.assertEqual(mock_signalapp.send.call_args_list[0][0][0].status, 'DELAY')

            self.assertEqual(mock_signalapp.send.call_args_list[1][0][0].mtype, 'status')
            self.assertEqual(mock_signalapp.send.call_args_list[1][0][0].status, 'RUN')

    def test_check_quote_cases(self):
        with patch('tradingcore.signalapp.SignalApp', spec=SignalApp) as mock_signalapp, \
                patch('scripts.quotes_notification.QuotesNotifyScript.date_now') as mock_now, \
                patch('scripts.quotes_notification.QuotesNotifyScript.get_last_quote_date') as mock_get_last_quote_date, \
                patch('scripts.quotes_notification.QuotesNotifyScript.set_last_quote_state') as mock_set_last_quote_date, \
                patch('exobuilder.data.assetindex_mongo.AssetIndexMongo.get_exec_time') as mock_get_exec_time:
            mock_args = Mock()
            mock_args.instrument = 'TEST'
            mock_args.delay = 3

            qn = QuotesNotifyScript(mock_args, logging.DEBUG)
            qn.signalapp = mock_signalapp

            mock_now.return_value = datetime.datetime(2016, 1, 1, 12, 56, 00)
            self.assertEqual(qn.is_quote_delayed(datetime.datetime(2016, 1, 1, 12, 47, 00)), False)

            mock_now.return_value = datetime.datetime(2016, 2, 1, 12, 56, 00)
            self.assertEqual(qn.is_quote_delayed(datetime.datetime(2016, 2, 1, 12, 47, 00)), True)

            # Time constraints
            mock_now.return_value = datetime.datetime(2016, 2, 1, 8, 0, 0)
            self.assertEqual(qn.is_quote_delayed(datetime.datetime(2016, 1, 1, 12, 47, 00)), False)

            mock_now.return_value = datetime.datetime(2016, 2, 1, 13, 0, 0)
            self.assertEqual(qn.is_quote_delayed(datetime.datetime(2016, 2, 1, 12, 47, 00)), False)

    def test_set_last_quote_state_real(self):
            mock_args = Mock()
            mock_args.instrument = 'TEST'
            mock_args.delay = 3

            qn = QuotesNotifyScript(mock_args, logging.DEBUG)
            status_client = MongoClient(MONGO_CONNSTR)
            qn.status_db = status_client[MONGO_EXO_DB]

            context = {
                'last_bar_time': datetime.datetime(2016, 2, 1, 12, 47, 00),
                'now': datetime.datetime(2016, 2, 1, 12, 47, 00),
                'last_run_date': datetime.datetime(2016, 2, 1, 12, 47, 00),
                'decision_time': datetime.datetime(2016, 2, 1, 12, 47, 00),
                'execution_time': datetime.datetime(2016, 2, 1, 12, 47, 00),
                'instrument': qn.args.instrument,
                'quote_status': 'RUN',
            }
            qn.set_last_quote_state(context, update=False)

            d = qn.status_db[STATUS_QUOTES_COLLECTION].find_one({'instrument': qn.args.instrument})
            del d['_id']

            context_update = {
                'last_bar_time': datetime.datetime(2016, 2, 1, 12, 48, 00),
                'now': datetime.datetime(2016, 2, 1, 12, 48, 00),
                'last_run_date': datetime.datetime(2016, 2, 1, 12, 48, 00),
                'decision_time': datetime.datetime(2016, 2, 1, 12, 48, 00),
                'execution_time': datetime.datetime(2016, 2, 1, 12, 48, 00),
                'instrument': qn.args.instrument,
                'quote_status': 'IDLE',
            }
            qn.set_last_quote_state(context_update, update=True)
            d = qn.status_db[STATUS_QUOTES_COLLECTION].find_one({'instrument': qn.args.instrument})
            self.assertEqual(d['last_bar_time'], datetime.datetime(2016, 2, 1, 12, 48, 00))
            self.assertEqual(d['now'], datetime.datetime(2016, 2, 1, 12, 48, 00))
            self.assertEqual(d['last_run_date'], datetime.datetime(2016, 2, 1, 12, 47, 00))
            self.assertEqual(d['decision_time'], datetime.datetime(2016, 2, 1, 12, 47, 00))
            self.assertEqual(d['decision_time'], datetime.datetime(2016, 2, 1, 12, 47, 00))


if __name__ == '__main__':
    unittest.main()
