import unittest
from exobuilder.contracts.futureschain import FuturesChain
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.tests.assetindexdict import AssetIndexDicts
from datetime import datetime, date, timedelta, time as dttime
from exobuilder.contracts.instrument import Instrument
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.datasource_sql import DataSourceSQL
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.exostorage import EXOStorage
from exobuilder.exo.exoenginebase import ExoEngineBase
from exobuilder.exo.transaction import Transaction
import time
from exobuilder.algorithms.rollover_helper import RolloverHelper
from exobuilder.smartexo.smartexo_ichi import SmartEXOIchi
from exobuilder.smartexo.smartexo_swp import SmartEXOSwingpoint
from exobuilder.smartexo.utils import SmartEXOUtils
import importlib
import logging
importlib.reload(logging);
import matplotlib.pyplot as plt
from bdateutil import relativedelta


class SmartEXOGeneric(SmartEXOSwingpoint):
    # Change the EXO name to reflect SmartEXO behavior
    EXO_NAME = 'SmartEXO_Bullish_SWP__class_based_test_20170314'

    ASSET_LIST = ['ZN']

    def __init__(self, symbol, direction, date, datasource, **kwargs):
        super().__init__(symbol, direction, date, datasource,
                         sphthreshold=2,
                         splthreshold=2,
                         )

    @staticmethod
    def new_position_bullish_zone(date, fut, opt_chain):
        # Edit transactions to trade
        trans_list = [
            # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
            #
            #
        ]
        return trans_list

    @staticmethod
    def new_position_bearish_zone(date, fut, opt_chain):
        trans_list = [
            # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
            #
            #
        ]

        return trans_list

    @staticmethod
    def new_position_neutral_zone(date, fut, opt_chain):
        # Edit transactions to trade
        trans_list = [
            # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
            #
            #
            Transaction(opt_chain.get_by_delta(0.05), date, 3.0),
            Transaction(opt_chain.get_by_delta(0.15), date, -3.0),
            Transaction(opt_chain.get_by_delta(-0.05), date, 2.0),
            Transaction(opt_chain.get_by_delta(-0.15), date, -2.0),
        ]
        return trans_list

    def manage_opened_position(self, date, fut, opt_chain, regime, opened_position):
        logging.debug('Current position delta: {0}'.format(opened_position.delta))

        delta = opened_position.delta
        # logging.debug("Last transaction date: {0}".format(opened_position.last_trans_date))
        days_after_last_trans = 0

        if opened_position.last_trans_date is not None:
            days_after_last_trans = relativedelta(date, opened_position.last_trans_date).bdays

        trans_list = []

        if regime == 1:
            # Delta bounds checks for BULLISH regime
            # Check required delta bounds values for position
            if days_after_last_trans > 5 and delta < 0.05 or delta > 0.55:
                # Do not change next
                logging.debug('Rebalancing bullish position')
                trans_list += opened_position.close_all_translist()
                trans_list += self.new_position_bullish_zone(date, fut, opt_chain)
                return trans_list
        if regime == -1:
            # Delta bounds checks for BEARISH regime
            # Check required delta bounds values for position
            if days_after_last_trans > 5 and delta < -0.55 or delta > -0.05:
                # Do not change next
                logging.debug('Rebalancing bearish position')
                trans_list += opened_position.close_all_translist()
                trans_list += self.new_position_bearish_zone(date, fut, opt_chain)
                return trans_list
        if regime == 0:
            # Delta bounds checks for NEUTRAL regime
            # Check required delta bounds values for position
            if days_after_last_trans > 5 and delta < -0.25 or delta > 0.25:
                # Do not change next
                logging.debug('Rebalancing neutral position')
                trans_list += opened_position.close_all_translist()
                trans_list += self.new_position_neutral_zone(date, fut, opt_chain)
                return trans_list

class MyTestCase(unittest.TestCase):
    def test_smart_exo_build(self):
        base_date = datetime(2017, 2, 17, 11, 5, 0)
        smart_utils = SmartEXOUtils(SmartEXOGeneric, verbosive_logging=True)
        smart_utils.build_smartexo(base_date, log_file_path='/home/ubertrader/')
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
