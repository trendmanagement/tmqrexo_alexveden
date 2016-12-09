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
from .datasourcefortest import DataSourceForTest

from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.datasource_sql import DataSourceSQL
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from scripts.settings import *
from exobuilder.algorithms.rollover_helper import RolloverHelper


class OptionChainTestCase(unittest.TestCase):
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

        for k, v in self.opt_chain.contracts.items():
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
        self.assertRaises(IndexError, self.opt_chain.__getitem__, -self.opt_chain.atmindex - 1)
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

    def test_chain_has_applyed_options_limit(self):
        self.fut._price = 1060.000001
        opt_chain = OptionsChain(self.opt_chain_dict, self.fut, 5)
        self.assertEqual(len(opt_chain.strikes), 11)  # 5 stikes per side + 1 ATM
        self.assertEqual(True, np.all(
            opt_chain.strikes == np.array([1020, 1025, 1030, 1040, 1050, 1060, 1070, 1075, 1080, 1090, 1100])))

    def test_chain_repr(self):
        opt_str = ""

        atmi = self.opt_chain.atmindex

        for i, strike in enumerate(self.opt_chain.strikes):
            opt_str += "{0}: {1}\n".format(i - atmi, self.opt_chain[strike])

        self.assertEqual(self.opt_chain.__repr__(), opt_str)

    def test_max_min_offset(self):
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)

        base_date = datetime(2015, 6, 13, 12, 45, 0)

        futures_limit = 3
        options_limit = 20

        datasource = DataSourceSQL(SQL_HOST, SQL_USER, SQL_PASS, assetindex, futures_limit, options_limit)

        instr = datasource.get("ES", base_date)
        rh = RolloverHelper(instr)
        fut, opt_chain = rh.get_active_chains()

        offset = opt_chain.maxoffset
        self.assertEqual(20, offset)

        offset = opt_chain.minoffset
        self.assertEqual(-20, offset)

    def test_chain_get_by_delta(self):
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)

        base_date = datetime(2015, 6, 13, 12, 45, 0)

        futures_limit = 3
        options_limit = 20

        datasource = DataSourceSQL(SQL_HOST, SQL_USER, SQL_PASS, assetindex, futures_limit, options_limit)

        instr = datasource.get("ES", base_date)
        rh = RolloverHelper(instr)
        fut, opt_chain = rh.get_active_chains()

        atm_strike = opt_chain.atmstrike

        opt = opt_chain.get_by_delta(0.5)
        self.assertEqual(opt.strike, atm_strike)
        self.assertEqual(opt.putorcall, 'C')

        opt = opt_chain.get_by_delta(-0.5)
        self.assertEqual(opt.strike, atm_strike)
        self.assertEqual(opt.putorcall, 'P')

        self.assertRaises(ValueError, opt_chain.get_by_delta, 0)
        self.assertRaises(ValueError, opt_chain.get_by_delta, float('nan'))
        self.assertRaises(ValueError, opt_chain.get_by_delta, 1)
        self.assertRaises(ValueError, opt_chain.get_by_delta, 2)
        self.assertRaises(ValueError, opt_chain.get_by_delta, -2)
        self.assertRaises(ValueError, opt_chain.get_by_delta, -1)

        # ITM Put
        opt = opt_chain.get_by_delta(-0.7)
        self.assertEqual(opt.strike, 2115)
        self.assertEqual(opt.putorcall, 'P')
        self.assertAlmostEqual(opt.delta, -0.75, 2)

        opt = opt_chain.get_by_delta(-0.999999)
        self.assertEqual(opt.strike, 2195.0)
        self.assertEqual(opt.putorcall, 'P')
        self.assertAlmostEqual(opt.delta, -0.989, 3)

        # OTM Put
        opt = opt_chain.get_by_delta(-0.3)
        self.assertEqual(opt.strike, 2070)
        self.assertEqual(opt.putorcall, 'P')
        self.assertAlmostEqual(opt.delta, -0.27, 2)

        opt = opt_chain.get_by_delta(-0.00001)
        self.assertEqual(opt, opt_chain[-20].P)

        # ITM Call
        opt = opt_chain.get_by_delta(0.7)
        self.assertEqual(opt.strike, 2070)
        self.assertEqual(opt.putorcall, 'C')
        self.assertAlmostEqual(opt.delta, 0.73, 2)

        opt = opt_chain.get_by_delta(0.9999999)
        self.assertEqual(opt, opt_chain[-20].C)

        # OTM Call
        opt = opt_chain.get_by_delta(0.3)
        self.assertEqual(opt.strike, 2115)
        self.assertEqual(opt.putorcall, 'C')
        self.assertAlmostEqual(opt.delta, 0.24, 2)

        opt = opt_chain.get_by_delta(0.000001)
        self.assertEqual(opt, opt_chain[20].C)

    def test_chain_handle_missing_data(self):
        assetindex = AssetIndexMongo(MONGO_CONNSTR, MONGO_EXO_DB)



        futures_limit = 3
        options_limit = 20

        datasource = DataSourceSQL(SQL_HOST, SQL_USER, SQL_PASS, assetindex, futures_limit, options_limit)

        base_date = datetime(2014, 2, 18, 11, 10, 0)
        instr = datasource.get("CL", base_date)
        rh = RolloverHelper(instr)
        fut, opt_chain = rh.get_active_chains()
        # opt_chain.get_by_delta(0.05) on the CL on this date is has absent data
        # opt_chain selects next available date
        self.assertEqual(opt_chain.get_by_delta(0.05), opt_chain.get_by_delta(0.04))

        base_date = datetime(2016, 2, 17, 11, 10, 0)
        instr = datasource.get("ZN", base_date)
        rh = RolloverHelper(instr)
        fut, opt_chain = rh.get_active_chains()
        # opt_chain[11] is an absent strike inside DB, if it absent opt_chain selects next available strike
        self.assertEqual(opt_chain[11], opt_chain[12])
        self.assertEqual(opt_chain[-11], opt_chain[-12])