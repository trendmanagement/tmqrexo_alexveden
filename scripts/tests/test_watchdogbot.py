import unittest
from unittest.mock import Mock, patch
from scripts.watchdogbot import WatchdogBot
from tradingcore.messages import MsgStatus
from datetime import datetime


class WatchBotTestCase(unittest.TestCase):
    def test_check_status_app(self):
        with patch('scripts.watchdogbot.WatchdogBot.get_shell_command_output') as mock_cmd_output:
            wdb = WatchdogBot('')

            mock_cmd_output.return_value = None
            self.assertEqual('N/A', wdb.check_status_apps())

            mock_cmd_output.return_value = ''
            self.assertEqual('N/A', wdb.check_status_apps())

            mock_cmd_output.return_value = """
QUOTES_ZW                                                                      FATAL     Exited too quickly (process log may have details)
TRADING_ONLINE                                                                 FATAL     Exited too quickly (process log may have details)
WATCHDOG_BOT                                                                   RUNNING   pid 10096, uptime 4 days, 21:19:23
gunicorn_webui                                                                 RUNNING   pid 10081, uptime 4 days, 21:19:24
jupyter_notebook                                                               RUNNING   pid 6080, uptime 4:20:35

            """
            self.assertEqual('FATAL:2 RUNNING:3 ', wdb.check_status_apps())


    def test_antiflood(self):
        wdb = WatchdogBot('')

        msg = MsgStatus('DELAY', 'Quote delayed')

        self.assertEqual(True, wdb.check_antiflood('test', 'test', msg, datetime(2015, 1, 1, 12, 30)))
        self.assertEqual(False, wdb.check_antiflood('test', 'test', msg, datetime(2015, 1, 1, 12, 31)))

        self.assertEqual(True, wdb.check_antiflood('test', 'test', msg, datetime(2015, 1, 1, 13, 31)))
        self.assertEqual(False, wdb.check_antiflood('test', 'test', msg, datetime(2015, 1, 1, 13, 31)))

        msg.status = 'RUN'
        self.assertEqual(True, wdb.check_antiflood('test', 'test', msg, datetime(2015, 1, 1, 13, 31)))

if __name__ == '__main__':
    unittest.main()
