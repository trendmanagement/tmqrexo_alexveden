import unittest
from exobuilder.contracts.futureschain import FuturesChain
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.contracts.optioncontract import OptionContract
from exobuilder.contracts.optionschain import OptionsChain
from exobuilder.contracts.putcallpair import PutCallPair
from .assetindexdict import AssetIndexDicts
from datetime import datetime, date
from exobuilder.contracts.instrument import Instrument
from collections import OrderedDict
import numpy as np

class OptionChainTestCase(unittest.TestCase):
    def setUp(self):
        self.assetindex = AssetIndexDicts()
        self.symbol = 'EP'
        self.date = datetime(2014, 1, 5, 0, 0, 0)
        self.futures_limit = 12
        self.instrument = Instrument(self.symbol, self.date, self.futures_limit, self.assetindex)

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
        self.opt_chain_dict = self.assetindex.get_options_list(None, None)[0]
        self.opt_chain = OptionsChain(self.opt_chain_dict, self.fut)

    def test_constructor(self):
        opt_chain = OptionsChain(self.opt_chain_dict, self.fut)
        self.assertEqual(opt_chain._data, self.opt_chain_dict)
        self.assertEqual(opt_chain._fut, self.fut)

    def test_chain_has_underlying(self):
        self.assertEqual(self.opt_chain.underlying, self.fut)

    def test_chain_has_instrument(self):
        self.assertEqual(self.opt_chain.instrument, self.fut.instrument)

    def test_chain_has_expiration(self):
        self.assertEqual(self.opt_chain.expiration, datetime(2014, 1, 17, 0, 0))

    def test_chain_has_contracts(self):
        self.assertEqual(type(self.opt_chain.contracts), OrderedDict)

        for k,v in self.opt_chain.contracts.items():
            self.assertEqual(float, type(k))
            self.assertEqual(PutCallPair, type(v))

    def test_chain_has_strikes(self):
        # Returns unique strike list for the asset
        strikes = np.array(sorted(set([x['strikeprice'] for x in self.opt_chain_dict['chain']])))
        self.assertTrue(np.all(self.opt_chain.strikes == strikes))

    def test_chain_has_len(self):
        strikes = np.array(sorted(set([x['strikeprice'] for x in self.opt_chain_dict['chain']])))
        self.assertEqual(len(self.opt_chain), len(strikes))

    def test_chain_is_iterable(self):
        for pair in self.opt_chain:
            self.assertEqual(type(pair), PutCallPair)

    def test_chain_is_iterable_items(self):
        for strike, pair in self.opt_chain.items():
            self.assertEqual(type(strike), float)
            self.assertEqual(type(pair), PutCallPair)

    def test_chain_has_set_item_error(self):
        self.assertRaises(AssertionError, self.opt_chain.__setitem__, 0, None)

    def test_chain_has_atmstrike(self):
        self.fut._price = 1059.56
        self.assertEqual(1060, self.opt_chain.atmstrike)

    def test_chain_has_atmstrike_little_higher(self):
        self.fut._price = 1060.16
        self.assertEqual(1060, self.opt_chain.atmstrike)

    def test_chain_has_atmstrike_exactly_between_strikes(self):
        self.fut._price = 1065.000000
        self.assertEqual(1060, self.opt_chain.atmstrike)

    def test_chain_has_atmstrike_exactly_almost_between_upper_epsilon(self):
        self.fut._price = 1065.000001
        self.assertEqual(1070, self.opt_chain.atmstrike)

    def test_chain_has_atmindex(self):
        self.fut._price = 1065.000000
        self.assertEqual(29, self.opt_chain.atmindex)

    def test_chain_has_atmstrike_is_caching_in_atmstrike(self):
        self.fut._price = 1060.000001
        self.assertEqual(-1, self.opt_chain._atm_index)
        self.assertEqual(1060, self.opt_chain.atmstrike)
        self.assertEqual(29, self.opt_chain._atm_index)
        self.assertEqual(1060, self.opt_chain.atmstrike)

    def test_chain_has_atmstrike_is_caching_in_atmindex(self):
        self.fut._price = 1060.000001
        self.assertEqual(-1, self.opt_chain._atm_index)
        self.assertEqual(29, self.opt_chain.atmindex)
        self.assertEqual(29, self.opt_chain._atm_index)
        self.assertEqual(29, self.opt_chain.atmindex)

    def test_chain_has_get_item_by_offset(self):
        self.fut._price = 1060.000001
        self.assertEqual(self.opt_chain[0].strike, 1060)
        self.assertEqual(self.opt_chain[1].strike, 1070)
        self.assertEqual(self.opt_chain[-1].strike, 1050)

    def test_chain_has_get_item_by_offset_index_error(self):
        self.fut._price = 1060.000001
        self.assertRaises(IndexError, self.opt_chain.__getitem__, -100)
        self.assertRaises(IndexError, self.opt_chain.__getitem__, 1000)
        self.assertRaises(IndexError, self.opt_chain.__getitem__, -self.opt_chain.atmindex-1)
        self.assertRaises(IndexError, self.opt_chain.__getitem__, len(self.opt_chain.strikes) - self.opt_chain.atmindex)

    def test_chain_has_get_item_by_offset_different_int_types(self):
        self.fut._price = 1060.000001
        self.assertEqual(self.opt_chain[np.int32(0)].strike, 1060)
        self.assertEqual(self.opt_chain[np.int64(0)].strike, 1060)
        self.assertEqual(self.opt_chain[int(0)].strike, 1060)
        self.assertEqual(self.opt_chain[0].strike, 1060)

    def test_chain_has_get_item_by_offset_different_float_types(self):
        self.fut._price = 1060.000001
        self.assertEqual(self.opt_chain[1060.0].strike, 1060)
        self.assertEqual(self.opt_chain[np.float32(1060.0)].strike, 1060)
        self.assertEqual(self.opt_chain[np.float64(1060.0)].strike, 1060)
        self.assertEqual(self.opt_chain[float(1060)].strike, 1060)

    def test_chain_has_get_item_by_strike_price_error_notfound(self):
        self.assertRaises(KeyError, self.opt_chain.__getitem__, 1231231231312.0)

    def test_chain_has_get_item_error_unexpected_item_type(self):
        self.assertRaises(ValueError, self.opt_chain.__getitem__, 'wrong type')





if __name__ == '__main__':
    unittest.main()

