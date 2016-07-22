import unittest
from .assetindexdict import AssetIndexDicts
from exobuilder.data.datasource import DataSourceBase
from exobuilder.contracts.instrument import Instrument
from datetime import datetime
import numpy as np

from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.contracts.optioncontract import OptionContract

class DatasourceMongoTestCase(unittest.TestCase):
    def setUp(self):
        self.assetindex = AssetIndexDicts()
        self.date = datetime(2014, 1, 6, 10, 15, 0)
        futures_limit = 3
        options_limit = 10
        self.datasource = DataSourceBase(self.assetindex, futures_limit, options_limit)

    def test_constructor(self):
        self.assertEqual(self.datasource.assetindex, self.assetindex)
        self.assertEqual(self.datasource.futures_limit, 3)
        self.assertEqual(self.datasource.options_limit, 10)

    def test_get_item_as_instument(self):
        instr = self.datasource.get('EP', self.date)
        self.assertEqual(type(instr), Instrument)
        self.assertEqual(instr.name, 'EP')
        self.assertEqual(instr.date, self.date)
        self.assertEqual(instr.futures_limit, 3)
        self.assertEqual(instr.options_limit, 10)

    def test_get_notimplemented_abstract_methods(self):
        self.assertRaises(NotImplementedError, self.datasource.get_fut_data, None, None)
        self.assertRaises(NotImplementedError, self.datasource.get_option_data, None, None)
        self.assertRaises(NotImplementedError, self.datasource.get_extra_data, None, None)

    def test_get_item_from_hash_future_contract(self):
        instr = self.datasource.get('EP', self.date)
        self.assertEqual(type(instr), Instrument)
        self.assertEqual(instr.name, 'EP')
        self.assertEqual(instr.date, self.date)
        self.assertEqual(instr.futures_limit, 3)
        self.assertEqual(instr.options_limit, 10)

        contract_dict = {'_id': '577a4fa34b01f47f84cab23c',
                              'contractname': 'F.EPZ16',
                              'cqgsymbol': 'F.EPZ16',
                              'expirationdate': datetime(2016, 12, 16, 0, 0),
                              'idcontract': 6570,
                              'idinstrument': 11,
                              'month': 'Z',
                              'monthint': 12,
                              'year': 2016}

        fut_contract = FutureContract(contract_dict, instr)

        hash = fut_contract.__hash__()

        f2 = self.datasource.get(hash, self.date)
        self.assertEqual(type(f2), FutureContract)
        self.assertEqual(f2.name, 'F.EPZ16')
        self.assertEqual(f2.date, self.date)
        self.assertEqual(f2, fut_contract)

    def test_get_item_from_hash_option_contract(self):
        instr = self.datasource.get('EP', self.date)
        self.assertEqual(type(instr), Instrument)
        self.assertEqual(instr.name, 'EP')
        self.assertEqual(instr.date, self.date)
        self.assertEqual(instr.futures_limit, 3)
        self.assertEqual(instr.options_limit, 10)

        contract_dict = {'_id': '577a4fa34b01f47f84cab23c',
                         'contractname': 'F.EPZ16',
                         'cqgsymbol': 'F.EPZ16',
                         'expirationdate': datetime(2016, 12, 16, 0, 0),
                         'idcontract': 4736,
                         'idinstrument': 11,
                         'month': 'Z',
                         'monthint': 12,
                         'year': 2016}

        fut_contract = FutureContract(contract_dict, instr)

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

        option_contract = OptionContract(opt_contract_dict, fut_contract)

        hash = option_contract.__hash__()

        opt2 = self.datasource.get(hash, self.date)
        self.assertEqual(type(opt2), OptionContract)
        self.assertEqual(opt2.name, 'P.US.EPH1427750')
        self.assertEqual(opt2.date, self.date)
        self.assertEqual(opt2, option_contract)
        self.assertEqual(opt2.underlying, fut_contract)

    def test_get_item_from_hash_option_contract_notimplemented(self):
        self.assertRaises(NotImplementedError, self.datasource.get, 300000000, self.date)
        self.assertRaises(NotImplementedError, self.datasource.get, 99999999, self.date)




