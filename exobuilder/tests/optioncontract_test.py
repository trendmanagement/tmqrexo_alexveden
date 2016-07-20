import unittest
from exobuilder.contracts.futureschain import FuturesChain
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.contracts.optioncontract import OptionContract
from .assetindexdict import AssetIndexDicts
from datetime import datetime, date
from exobuilder.contracts.instrument import Instrument
from .datasourcefortest import DataSourceForTest
from exobuilder.algorithms.blackscholes import blackscholes
import numpy as np

class OptionContractTestCase(unittest.TestCase):
    def setUp(self):
        self.assetindex = AssetIndexDicts()
        self.symbol = 'EP'
        self.date = datetime(2014, 1, 5, 0, 0, 0)
        self.futures_limit = 12
        self.datasource = DataSourceForTest(self.assetindex, self.date, self.futures_limit, 0)
        self.instrument = self.datasource[self.symbol]

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

        self.opt_contract_dict = {'_id': '577a573e4b01f47f84d0cbd5',
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

        self.option_contract = OptionContract(self.opt_contract_dict, self.fut_contract)

    def test_constructor(self):
        opt_contract = OptionContract(self.opt_contract_dict, self.fut_contract)
        self.assertEqual(type(opt_contract._data), dict)
        self.assertEqual(type(opt_contract._future_contract), FutureContract)

    def test_optioncontract_has_name(self):
        self.assertEqual(self.option_contract.name, self.opt_contract_dict['optionname'])

    def test_optioncontract_has_underlying(self):
        self.assertEqual(self.option_contract.underlying, self.fut_contract)

    def test_optioncontract_has_strike(self):
        self.assertEqual(self.option_contract.strike, self.opt_contract_dict['strikeprice'])

    def test_optioncontract_has_instrument(self):
        self.assertEqual(self.option_contract.instrument, self.instrument)

    def test_optioncontract_has_expiration(self):
        self.assertEqual(self.option_contract.expiration, self.opt_contract_dict['expirationdate'])

    def test_optioncontract_has_callorput_uppercase(self):
        self.assertEqual(self.option_contract.callorput, 'P')

    def test_optioncontract_has_putorcall_uppercase(self):
        self.assertEqual(self.option_contract.putorcall, 'P')

    def test_optioncontract_has_dbid(self):
        self.assertEqual(self.option_contract.dbid, self.opt_contract_dict['idoption'])

    def test_optioncontract_has_date(self):
        self.assertEqual(self.option_contract.date, self.date)

    def test_optioncontract_has_toexpiration_years(self):
        self.assertEqual(self.option_contract.to_expiration_years,
                         (self.option_contract.expiration - self.date).total_seconds() / (365.0 * 24 * 60 * 60))

    def test_optioncontract_has_toexpiration_days(self):
        self.assertEqual(self.option_contract.to_expiration_days,
                         (self.option_contract.expiration - self.date).total_seconds() / (24 * 60 * 60))

    def test_optioncontract_has_toexpiration_days_iszero_on_expiration_time(self):
        opt_contract_dict = {'_id': '577a573e4b01f47f84d0cbd5',
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

        option_contract = OptionContract(opt_contract_dict, self.fut_contract)
        self.instrument.date = datetime(2014, 3, 21, 9, 30, 0)
        self.assertEqual(option_contract.to_expiration_days, 0)

    def test_optioncontract_has_toexpiration_days_iszero_integer(self):
        opt_contract_dict = {'_id': '577a573e4b01f47f84d0cbd5',
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

        option_contract = OptionContract(opt_contract_dict, self.fut_contract)
        self.instrument.date = datetime(2014, 3, 20, 9, 30, 0)
        self.assertEqual(option_contract.to_expiration_days, 1)

    def test_optioncontract_has_toexpiration_years_iszero_on_expiration_time(self):
        opt_contract_dict = {'_id': '577a573e4b01f47f84d0cbd5',
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

        option_contract = OptionContract(opt_contract_dict, self.fut_contract)
        self.instrument.date = datetime(2014, 3, 21, 9, 30, 0)
        self.assertEqual(option_contract.to_expiration_years, 0)

    def test_optioncontract_has_riskfreerate(self):
        opt_contract_dict = {'_id': '577a573e4b01f47f84d0cbd5',
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

        option_contract = OptionContract(opt_contract_dict, self.fut_contract)
        self.instrument.date = datetime(2014, 3, 21, 9, 30, 0)
        self.assertEqual(option_contract.riskfreerate, 0.255)

    def test_optioncontract_has_iv_and_caching(self):
        opt_contract_dict = {'_id': '577a573e4b01f47f84d0cbd5',
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

        option_contract = OptionContract(opt_contract_dict, self.fut_contract)
        self.instrument.date = datetime(2014, 3, 21, 9, 30, 0)
        self.assertEqual(option_contract._option_price_data, None)
        self.assertEqual(option_contract.iv, 0.356)
        self.assertNotEqual(option_contract._option_price_data, None)

    def test_optioncontract_has_price_put(self):
        opt_contract_dict = {'_id': '577a573e4b01f47f84d0cbd5',
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

        option_contract = OptionContract(opt_contract_dict, self.fut_contract)
        self.instrument.date = datetime(2014, 3, 21, 9, 30, 0)

        S = option_contract.underlying.price
        self.assertEqual(2770.0, S)

        T = option_contract.to_expiration_years

        X = option_contract.strike

        r = option_contract.riskfreerate
        self.assertEqual(r, 0.255)

        v = option_contract.iv
        self.assertEqual(v, 0.356)

        callputflag = option_contract.callorput
        self.assertEqual(callputflag, 'P')

        self.assertEqual(option_contract.price, blackscholes(callputflag, S, X, T, r, v))
        self.assertNotEqual(option_contract.price, 0)

    def test_optioncontract_has_price_call(self):
        opt_contract_dict = {'_id': '577a573e4b01f47f84d0cbd5',
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

        option_contract = OptionContract(opt_contract_dict, self.fut_contract)
        self.instrument.date = datetime(2014, 3, 21, 9, 30, 0)

        S = option_contract.underlying.price
        self.assertEqual(2770.0, S)

        T = option_contract.to_expiration_years

        X = option_contract.strike

        r = option_contract.riskfreerate
        self.assertEqual(r, 0.255)

        v = option_contract.iv
        self.assertEqual(v, 0.356)

        callputflag = option_contract.callorput
        self.assertEqual(callputflag, 'C')

        self.assertEqual(option_contract.price, blackscholes(callputflag, S, X, T, r, v))
        self.assertNotEqual(option_contract.price, 0)

    def test_optioncontract_has_price_caching(self):
        opt_contract_dict = {'_id': '577a573e4b01f47f84d0cbd5',
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

        option_contract = OptionContract(opt_contract_dict, self.fut_contract)
        self.instrument.date = datetime(2014, 3, 21, 9, 30, 0)

        S = option_contract.underlying.price
        self.assertEqual(2770.0, S)

        T = option_contract.to_expiration_years

        X = option_contract.strike

        r = option_contract.riskfreerate
        self.assertEqual(r, 0.255)

        v = option_contract.iv
        self.assertEqual(v, 0.356)

        callputflag = option_contract.callorput
        self.assertEqual(callputflag, 'C')

        self.assertTrue(np.isnan(option_contract._option_price))
        self.assertEqual(option_contract.price, blackscholes(callputflag, S, X, T, r, v))
        self.assertFalse(np.isnan(option_contract._option_price))
        self.assertNotEqual(option_contract.price, 0)
        self.assertFalse(np.isnan(option_contract._option_price))

    def test_optioncontract_has_price_exception(self):
        opt_contract_dict = {'_id': '577a573e4b01f47f84d0cbd5',
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

        option_contract = OptionContract(opt_contract_dict, self.fut_contract)
        self.instrument.date = datetime(2014, 3, 21, 9, 30, 0)

        S = option_contract.underlying.price
        self.assertEqual(2770.0, S)

        T = option_contract.to_expiration_years

        X = option_contract.strike

        r = option_contract.riskfreerate
        self.assertEqual(r, 0.255)

        v = -option_contract.iv
        self.assertEqual(v, -0.356)

        callputflag = option_contract.callorput
        self.assertEqual(callputflag, 'C')

        # TODO: Add more error handling conditions to BS
        self.assertTrue(np.isnan(blackscholes(callputflag, S, X, -T, r, v)))

    def test_optioncontract_has_pointvalue(self):
        self.assertEqual(self.option_contract.pointvalue, self.instrument.point_value_options)

    def test_optioncontract_as_dict(self):
        self.assertEqual({'name': self.option_contract.name, 'dbid': self.option_contract.dbid, 'type': 'O', 'hash': self.option_contract.__hash__()}, self.option_contract.as_dict())

    def test_optioncontract_hash(self):
        self.assertEqual(200000000 + self.option_contract.dbid, self.option_contract.__hash__())

    def test_equality(self):
        opt_contract_dict = {'_id': '577a573e4b01f47f84d0cbd5',
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

        option_contract = OptionContract(opt_contract_dict, self.fut_contract)

        self.assertEqual(option_contract, self.option_contract)
        self.assertFalse(option_contract is None)
        self.assertNotEqual(option_contract, None)
