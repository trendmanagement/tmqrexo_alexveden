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
from exobuilder.smartexo.utils import SmartEXOUtils
import importlib
import logging
importlib.reload(logging);
import matplotlib.pyplot as plt


class SmartEXOGeneric(SmartEXOIchi):
    # Change the EXO name to reflect SmartEXO behavior
    EXO_NAME = 'SmartEXO_Bullish_Ichi__class_based_test'

    ASSET_LIST = ['ES']

    def __init__(self, symbol, direction, date, datasource, **kwargs):
        super().__init__(symbol, direction, date, datasource,
                         #
                         # Change following values if you need to customize Ichimoku settings
                         #
                         conversion_line_period=9,
                         base_line_period=26,
                         leading_spans_lookahead_period=26,
                         leading_span_b_period=52,
                         **kwargs
                         )

    @staticmethod
    def new_position_bullish_zone(date, fut, opt_chain):
        """
        Returns transaction to open new Smart EXO position for bullish zone

        params date: current date
        params fut: current actual future contract
        params opt_chain: current actual options chain

        returns: List of Transactions to open
        """

        #
        # Opening short put spread  bullish zone
        #
        # https://files.slack.com/files-tmb/T0484J7T7-F2QBLK53R-93b4252806/pasted_image_at_2016_10_17_10_08_am_720.png

        trans_list = [
            # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
            Transaction(opt_chain[2].c, date, 0.0, leg_name='bullish'),
            Transaction(opt_chain[7].c, date, 0.0),
            Transaction(opt_chain[-7].p, date, 1.0),
            Transaction(opt_chain[-9].p, date, -1.0),

            # Transaction(opt_chain[3].p, date, -3.0),

            Transaction(opt_chain[-6].p, date, 3.0),
            Transaction(opt_chain[-11].p, date, -3.0),

        ]
        return trans_list

    @staticmethod
    def new_position_bearish_zone(date, fut, opt_chain):
        """
        Returns transaction to open new Smart EXO position for bearish zone

        params date: current date
        params fut: current actual future contract
        params opt_chain: current actual options chain

        returns: List of Transactions to open
        """
        #
        # Opening small ITM straddle in bearish zone
        #

        trans_list = [
            # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
            Transaction(opt_chain[4].c, date, 0.0, leg_name='bearish'),
            Transaction(opt_chain[7].c, date, 0.0),

            Transaction(opt_chain[3].p, date, -1.0),
            Transaction(opt_chain[-6].p, date, 1.0),
            # Transaction(opt_chain[-7].p, date, 1.0),
            # Transaction(opt_chain[-9].p, date, -1.0),
            # Transaction(opt_chain[2].c, date, 0.0, leg_name='bearish'),
            # Transaction(opt_chain[2].p, date, 0.0),
        ]

        return trans_list

    @staticmethod
    def new_position_neutral_zone(date, fut, opt_chain):
        """
        Returns transaction to open new Smart EXO position for neutral zone

        params date: current date
        params fut: current actual future contract
        params opt_chain: current actual options chain

        returns: List of Transactions to open
        """

        # Opening long asymmetric butterfly in neutral zone
        #
        # https://files.slack.com/files-tmb/T0484J7T7-F2PGU8QNQ-6344e6a04c/pasted_image_at_2016_10_14_09_43_am_720.png
        trans_list = [
            # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
            Transaction(opt_chain[-2].c, date, -0.0, leg_name='neutral'),
            Transaction(opt_chain[2].c, date, 0.0),

            Transaction(opt_chain[8].c, date, -0.0),
            Transaction(opt_chain[3].c, date, 0.0),
        ]

        return trans_list

    @staticmethod
    def manage_opened_position(date, fut, opt_chain, regime, opened_position):
        logging.debug('Current position delta: {0}'.format(opened_position.delta))

        # By default: do nothing
        return []

    pass

class MyTestCase(unittest.TestCase):
    def test_smart_exo_build(self):
        return
        base_date = datetime(2015, 1, 1, 12, 45, 0)
        smart_utils = SmartEXOUtils(SmartEXOGeneric, verbosive_logging=True)
        smart_utils.build_smartexo(base_date, log_file_path='/home/ubertrader/')
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
