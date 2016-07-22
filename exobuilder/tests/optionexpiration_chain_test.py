import unittest
from exobuilder.contracts.futureschain import FuturesChain
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.contracts.optioncontract import OptionContract
from exobuilder.contracts.optionexpirationchain import OptionExpirationChain
from exobuilder.contracts.optionschain import OptionsChain
from exobuilder.contracts.putcallpair import PutCallPair
from .assetindexdict import AssetIndexDicts
from datetime import datetime, date
from exobuilder.contracts.instrument import Instrument
from collections import OrderedDict
import numpy as np
from .datasourcefortest import DataSourceForTest

class OptionExpirationChainTestCase(unittest.TestCase):
    def setUp(self):
        self.assetindex = AssetIndexDicts()
        self.symbol = 'EP'
        self.date = datetime(2014, 1, 5, 0, 0, 0)
        self.futures_limit = 12
        self.datasource = DataSourceForTest(self.assetindex, self.futures_limit, 0)
        self.instrument = self.datasource.get(self.symbol, self.date)

        fut_contract_dic = {'_id': '577a4f9e4b01f47f84caad7b',
                          'contractname': 'F.US.EPH14',
                          'cqgsymbol': 'F.EPH14',
                          'expirationdate': datetime(2014, 3, 21, 0, 0),
                          'idcontract': 4736,
                          'idinstrument': 11,
                          'month': 'H',
                          'monthint': 3,
                          'year': 2014
                          }

        self.fut = FutureContract(fut_contract_dic, self.instrument)

        # Get 1st options expiration dict
        self.opt_chain_dict = self.assetindex.get_options_list(None, None)
        self.opt_chain = OptionExpirationChain(self.opt_chain_dict, self.fut)

    def test_constructor(self):
        opt_chain = OptionExpirationChain(self.opt_chain_dict, self.fut)
        self.assertEqual(opt_chain._data, self.opt_chain_dict)
        self.assertEqual(opt_chain._fut, self.fut)

    def test_has_chains(self):
        self.assertEqual(type(self.opt_chain._chains), OrderedDict)
        for expiry_date, chain in self.opt_chain._chains.items():
            self.assertEqual(datetime, type(expiry_date))
            self.assertEqual(OptionsChain, type(chain))

    def test_has_expirations(self):
        self.assertEqual(self.opt_chain.expirations, sorted(list(set([x['_id']['date'] for x in self.opt_chain_dict]))))

    def test_has_len(self):
        self.assertEqual(len(self.opt_chain), len(self.opt_chain.expirations))

    def test_has_iterable(self):
        for chain in self.opt_chain:
            self.assertEqual(type(chain), OptionsChain)

    def test_has_iterable_items(self):
        for expiration, chain in self.opt_chain.items():
            self.assertEqual(type(expiration), datetime)
            self.assertEqual(type(chain), OptionsChain)

    def test_chain_has_set_item_error(self):
        self.assertRaises(AssertionError, self.opt_chain.__setitem__, 0, None)

    def test_chain_get_item_by_date(self):
        expiry = datetime(2014, 1, 17, 0, 0)
        self.assertEqual(self.opt_chain[expiry.date()].expiration, expiry)

    def test_chain_get_item_by_date_time(self):
        expiry = datetime(2014, 1, 17, 0, 0)
        self.assertEqual(self.opt_chain[expiry].expiration, expiry)

    def test_chain_has_get_item_error_unexpected_item_type(self):
        self.assertRaises(ValueError, self.opt_chain.__getitem__, 'wrong type')

    def test_chain_get_item_by_offset(self):
        expiry = datetime(2014, 1, 17, 0, 0)
        self.assertEqual(self.opt_chain[0].expiration, expiry)

    def test_chain_repr(self):
        exp_str = ""

        for i, exp in enumerate(self.opt_chain.expirations):
            exp_str += '{0}: {1}\n'.format(i, exp.date())

        self.assertEqual(self.opt_chain.__repr__(), exp_str)

