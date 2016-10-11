import unittest
import time
from tradingcore.signalapp import SignalApp

class SignalAppTestCase(unittest.TestCase):
    def test_heart_beat_fail(self):
        def call_back(appclass, appname, data_object):
            print(data_object)
            raise Exception('ok')
            pass
        app = SignalApp('test', 'testclass')
        app.listen(call_back)

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
