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
#from exobuilder.smartexo.utils import SmartEXOUtils

import importlib
import logging
importlib.reload(logging);
#import matplotlib.pyplot as plt

from exobuilder.smartexo.smartexo_ichi import SmartEXOIchi


class SmartEXO_Ichi_Bearish_Fence(SmartEXOIchi):
    # Change the EXO name to reflect SmartEXO behavior
    EXO_NAME = 'SmartEXO_Ichi_Class_Based_Bearish_Fence_Dec19'

    # select instruments list for SMART EXO calculation


    def __init__(self, symbol, direction, date, datasource, **kwargs):
        super().__init__(symbol, direction, date, datasource,
                         #
                         # Change following values if you need to customize Ichimoku settings
                         #
                         conversion_line_period=9,
                         base_line_period=26,
                         leading_spans_lookahead_period=26,
                         leading_span_b_period=52
                         )

    @staticmethod
    def new_position_bullish_zone(date, fut, opt_chain):
        """
        opt_chain.get_by_delta(delta_value) help:

        Search option contract by delta value:
        If delta ==  0.5 - returns ATM call
        If delta == -0.5 - returns ATM put

        If delta > 0.5 - returns ITM call near target delta
        If delta < -0.5 - returns ITM put near target delta

        If delta > 0 and < 0.5 - returns OTM call
        If delta < 0 and > -0.5 - returns OTM put

        If delta <= -1 or >= 1 or 0 - raises error

        Examples:
        # ATM put (delta = -0.5)
        Transaction(opt_chain.get_by_delta(-0.5), date, 1.0),
        # OTM put (delta = -0.25)
        Transaction(opt_chain.get_by_delta(-0.25), date, 1.0),
        # ITM put (delta = -0.75)
        Transaction(opt_chain.get_by_delta(-0.75), date, 1.0),

        # ATM call (delta = 0.5)
        Transaction(opt_chain.get_by_delta(0.5), date, 1.0),
        # OTM call (delta = 0.25)
        Transaction(opt_chain.get_by_delta(0.25), date, 1.0),
        # ITM call (delta = 0.75)
        Transaction(opt_chain.get_by_delta(0.75), date, 1.0),
        """

        # Edit transactions to trade
        trans_list = [
            # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
            #
            #
            Transaction(opt_chain.get_by_delta(0.15), date, 1.0),
            Transaction(opt_chain.get_by_delta(-0.25), date, -1.0),
        ]
        return trans_list

    @staticmethod
    def new_position_bearish_zone(date, fut, opt_chain):
        trans_list = [
            # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
            #
            #
            Transaction(opt_chain.get_by_delta(0.15), date, 1.0),
            Transaction(opt_chain.get_by_delta(-0.25), date, -1.0),

        ]

        return trans_list

    @staticmethod
    def new_position_neutral_zone(date, fut, opt_chain):
        # Edit transactions to trade
        trans_list = [
            # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
            #
            #
            Transaction(opt_chain.get_by_delta(0.15), date, 1.0),
            Transaction(opt_chain.get_by_delta(-0.25), date, -1.0),
        ]
        return trans_list

    def manage_opened_position(self, date, fut, opt_chain, regime, opened_position):
        logging.debug('Current position delta: {0}'.format(opened_position.delta))

        delta = opened_position.delta

        trans_list = []

        if regime == 1:
            # Delta bounds checks for BULLISH regime
            # Check required delta bounds values for position
            if delta < 0.25 or delta > 0.75:
                # Do not change next
                logging.debug('Rebalancing bullish position')
                trans_list += opened_position.close_all_translist()
                trans_list += self.new_position_bullish_zone(date, fut, opt_chain)
                return trans_list
        if regime == -1:
            # Delta bounds checks for BEARISH regime
            # Check required delta bounds values for position
            if delta < -0.75 or delta > -0.25:
                # Do not change next
                logging.debug('Rebalancing bearish position')
                trans_list += opened_position.close_all_translist()
                trans_list += self.new_position_bearish_zone(date, fut, opt_chain)
                return trans_list
        if regime == 0:
            # Delta bounds checks for NEUTRAL regime
            # Check required delta bounds values for position
            if delta < -0.25 or delta > 0.25:
                # Do not change next
                logging.debug('Rebalancing neutral position')
                trans_list += opened_position.close_all_translist()
                trans_list += self.new_position_neutral_zone(date, fut, opt_chain)
                return trans_list
