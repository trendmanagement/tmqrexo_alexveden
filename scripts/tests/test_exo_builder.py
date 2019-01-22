import unittest
from tradingcore.messages import *
from scripts.exo_builder import EXOScript
from tradingcore.signalapp import APPCLASS_DATA
import logging
from datetime import datetime

class EXOBuilderTestCase(unittest.TestCase):
    def test_check_quote_data(self):
        scr = EXOScript(None, logging.DEBUG)



        self.assertEqual(scr.check_quote_data("TEST", "TEST", None), False)


        msg = MsgQuoteNotification("TEST", datetime.now())
        self.assertEqual(scr.check_quote_data("TEST", APPCLASS_DATA, msg), True)

        msg = MsgStatus("TEST", 'test status')
        self.assertEqual(scr.check_quote_data("TEST", APPCLASS_DATA, msg), False)


if __name__ == '__main__':
    unittest.main()
