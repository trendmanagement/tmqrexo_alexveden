import unittest
from exobuilder.contracts.futureschain import FuturesChain
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.contracts.optioncontract import OptionContract
from exobuilder.contracts.putcallpair import PutCallPair
from .assetindexdict import AssetIndexDicts
from datetime import datetime, date
from exobuilder.contracts.instrument import Instrument
import numpy as np

class PutCallPainTestCase(unittest.TestCase):
    def setUp(self):
        self.instrument = Instrument
        self.contract_dict = {'_id': '577a4fa34b01f47f84cab23c',
                              'contractname': 'F.EPZ16',
                              'cqgsymbol': 'F.EPZ16',
                              'expirationdate': datetime(2016, 12, 16, 0, 0),
                              'idcontract': 6570,
                              'idinstrument': 11,
                              'month': 'Z',
                              'monthint': 12,
                              'year': 2016}

        self.fut_contract = FutureContract(self.contract_dict, self.instrument)

        self.opt_contract_dict_put = {'_id': '577a573e4b01f47f84d0cbd5',
                                'callorput': 'p',
                                'cqgsymbol': 'P.US.EPH1427750',
                                'expirationdate': datetime(2014, 3, 21, 0, 0),
                                'idcontract': 4736,
                                'idinstrument': 11,
                                'idoption': 11558454,
                                'optionmonth': 'H',
                                'optionmonthint': 3,
                                'optionname': 'P.US.EPH1427750',
                                'optionyear': 2014,
                                'strikeprice': 2775.0
                                      }

        self.option_contract_put = OptionContract(self.opt_contract_dict_put, self.fut_contract)

    def test_constructor(self):
        pair = PutCallPair()
        self.assertEqual(pair._put, None)
        self.assertEqual(pair._call, None)
        self.assertTrue(np.isnan(pair._strike))

    def test_putcallpair_addoption(self):
        pair = PutCallPair()
        pair.addoption(self.option_contract_put)
        self.assertEqual(pair._put, self.option_contract_put)
        self.assertEqual(pair._call, None)

    def test_putcallpair_addoption_error_on_duclicate(self):
        pair = PutCallPair()
        pair.addoption(self.option_contract_put)
        self.assertRaises(ValueError, pair.addoption, self.option_contract_put)

    def test_putcallpair_addoption_call(self):
        pair = PutCallPair()
        pair.addoption(self.option_contract_put)

        opt_contract_dict_call = {'_id': '577a573e4b01f47f84d0cbd5',
                                 'callorput': 'c',
                                 'cqgsymbol': 'P.US.EPH1427750',
                                 'expirationdate': datetime(2014, 3, 21, 0, 0),
                                 'idcontract': 4736,
                                 'idinstrument': 11,
                                 'idoption': 11558454,
                                 'optionmonth': 'H',
                                 'optionmonthint': 3,
                                 'optionname': 'P.US.EPH1427750',
                                 'optionyear': 2014,
                                 'strikeprice': 2775.0
                                 }

        option_contract_call = OptionContract(opt_contract_dict_call, self.fut_contract)
        pair.addoption(option_contract_call)

        self.assertEqual(pair._put, self.option_contract_put)
        self.assertEqual(pair._call, option_contract_call)

    def test_putcallpair_addoption_call_error_onduplicate(self):
        pair = PutCallPair()
        pair.addoption(self.option_contract_put)

        opt_contract_dict_call = {'_id': '577a573e4b01f47f84d0cbd5',
                                  'callorput': 'c',
                                  'cqgsymbol': 'P.US.EPH1427750',
                                  'expirationdate': datetime(2014, 3, 21, 0, 0),
                                  'idcontract': 4736,
                                  'idinstrument': 11,
                                  'idoption': 11558454,
                                  'optionmonth': 'H',
                                  'optionmonthint': 3,
                                  'optionname': 'P.US.EPH1427750',
                                  'optionyear': 2014,
                                  'strikeprice': 2775.0
                                  }

        option_contract_call = OptionContract(opt_contract_dict_call, self.fut_contract)
        pair.addoption(option_contract_call)

        self.assertEqual(pair._put, self.option_contract_put)
        self.assertEqual(pair._call, option_contract_call)
        self.assertRaises(ValueError, pair.addoption, option_contract_call)

    def test_putcallpair_has_strike(self):
        pair = PutCallPair()
        pair.addoption(self.option_contract_put)
        self.assertEqual(pair._put, self.option_contract_put)
        self.assertEqual(pair._call, None)
        self.assertEqual(pair.strike, 2775.0)

    def test_putcallpair_addoption_call_error_different_strike(self):
        pair = PutCallPair()
        pair.addoption(self.option_contract_put)

        opt_contract_dict_call = {'_id': '577a573e4b01f47f84d0cbd5',
                                  'callorput': 'c',
                                  'cqgsymbol': 'P.US.EPH1427750',
                                  'expirationdate': datetime(2014, 3, 21, 0, 0),
                                  'idcontract': 4736,
                                  'idinstrument': 11,
                                  'idoption': 11558454,
                                  'optionmonth': 'H',
                                  'optionmonthint': 3,
                                  'optionname': 'P.US.EPH1427750',
                                  'optionyear': 2014,
                                  'strikeprice': 2785.0
                                  }

        option_contract_call = OptionContract(opt_contract_dict_call, self.fut_contract)

        self.assertEqual(pair._put, self.option_contract_put)
        self.assertRaises(ValueError, pair.addoption, option_contract_call)

    def test_putcallpair_has_expiration(self):
        pair = PutCallPair()
        self.assertEqual(None, pair._expiration)
        self.assertEqual(None, pair.expiration)
        pair.addoption(self.option_contract_put)

    def test_putcallpair_addoption_expiration_set(self):
        pair = PutCallPair()
        self.assertEqual(None, pair._expiration)
        self.assertEqual(None, pair.expiration)
        pair.addoption(self.option_contract_put)
        self.assertEqual(pair.expiration, datetime(2014, 3, 21, 0, 0))

    def test_putcallpair_addoption_expiration_error_on_different_expiration(self):
        pair = PutCallPair()
        self.assertEqual(None, pair._expiration)
        self.assertEqual(None, pair.expiration)
        pair.addoption(self.option_contract_put)
        opt_contract_dict_call = {'_id': '577a573e4b01f47f84d0cbd5',
                                  'callorput': 'c',
                                  'cqgsymbol': 'P.US.EPH1427750',
                                  'expirationdate': datetime(2014, 3, 22, 0, 0),
                                  'idcontract': 4736,
                                  'idinstrument': 11,
                                  'idoption': 11558454,
                                  'optionmonth': 'H',
                                  'optionmonthint': 3,
                                  'optionname': 'P.US.EPH1427750',
                                  'optionyear': 2014,
                                  'strikeprice': 2775.0
                                  }
        self.assertEqual(pair.expiration, datetime(2014, 3, 21, 0, 0))

        option_contract_call = OptionContract(opt_contract_dict_call, self.fut_contract)
        self.assertRaises(ValueError, pair.addoption, option_contract_call)

    def test_putcallpair_has_c(self):
        pair = PutCallPair()
        self.assertEqual(None, pair.C)
        self.assertEqual(None, pair.c)
        pair.addoption(self.option_contract_put)

        opt_contract_dict_call = {'_id': '577a573e4b01f47f84d0cbd5',
                                  'callorput': 'c',
                                  'cqgsymbol': 'P.US.EPH1427750',
                                  'expirationdate': datetime(2014, 3, 21, 0, 0),
                                  'idcontract': 4736,
                                  'idinstrument': 11,
                                  'idoption': 11558454,
                                  'optionmonth': 'H',
                                  'optionmonthint': 3,
                                  'optionname': 'P.US.EPH1427750',
                                  'optionyear': 2014,
                                  'strikeprice': 2775.0
                                  }

        option_contract_call = OptionContract(opt_contract_dict_call, self.fut_contract)
        pair.addoption(option_contract_call)
        self.assertEqual(option_contract_call, pair.C)
        self.assertEqual(option_contract_call, pair.c)
        self.assertEqual(option_contract_call, pair.call)

    def test_putcallpair_has_p(self):
        pair = PutCallPair()
        self.assertEqual(None, pair.P)
        self.assertEqual(None, pair.p)
        pair.addoption(self.option_contract_put)
        self.assertEqual(self.option_contract_put, pair.P)
        self.assertEqual(self.option_contract_put, pair.p)
        self.assertEqual(self.option_contract_put, pair.put)

    def test_putcallpair_has_underlying(self):
        pair = PutCallPair()
        self.assertEqual(None, pair.underlying)
        pair.addoption(self.option_contract_put)
        self.assertEqual(self.fut_contract, pair.underlying)

        opt_contract_dict_call = {'_id': '577a573e4b01f47f84d0cbd5',
                                  'callorput': 'c',
                                  'cqgsymbol': 'P.US.EPH1427750',
                                  'expirationdate': datetime(2014, 3, 21, 0, 0),
                                  'idcontract': 4736,
                                  'idinstrument': 11,
                                  'idoption': 11558454,
                                  'optionmonth': 'H',
                                  'optionmonthint': 3,
                                  'optionname': 'P.US.EPH1427750',
                                  'optionyear': 2014,
                                  'strikeprice': 2775.0
                                  }
        option_contract_call = OptionContract(opt_contract_dict_call, self.fut_contract)

        pair = PutCallPair()
        pair.addoption(option_contract_call)
        self.assertEqual(self.fut_contract, pair.underlying)

    def test_putcallpair_has_repr(self):
        pair = PutCallPair()
        pair.addoption(self.option_contract_put)

        opt_contract_dict_call = {'_id': '577a573e4b01f47f84d0cbd5',
                                  'callorput': 'c',
                                  'cqgsymbol': 'P.US.EPH1427750',
                                  'expirationdate': datetime(2014, 3, 21, 0, 0),
                                  'idcontract': 4736,
                                  'idinstrument': 11,
                                  'idoption': 11558454,
                                  'optionmonth': 'H',
                                  'optionmonthint': 3,
                                  'optionname': 'P.US.EPH1427750',
                                  'optionyear': 2014,
                                  'strikeprice': 2775.0
                                  }
        option_contract_call = OptionContract(opt_contract_dict_call, self.fut_contract)

        pair.addoption(option_contract_call)
        self.assertEqual(pair.__repr__(), "{0} {1} / {2}".format(pair.strike, pair.call.name, pair.put.name))



if __name__ == '__main__':
    unittest.main()
