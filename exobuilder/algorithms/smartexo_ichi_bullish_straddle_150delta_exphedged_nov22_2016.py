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
import logging


EXO_NAME = 'SmartEXO_Ichi_Bullish_Straddle_150Delta_ExpHedged_Nov22_2016'



'''
Define Bull/Bear/Neutral areas rules
'''
def ichimoku_regimes(date, price_series):
    '''
    Calculates Bull/Bear/Neutral areas based on Ichimoku zones

    param date: Current date time
    param price_series: price Pandas.Series

    Returns:
        -1 - for bearish zone
        0  - for neutral zone
        +1 - for bullish zone
        None - for unknown
    '''
    #
    #  TODO: Change values to fine tune zoning algorithm
    #
    conversion_line_period = 9 # subject of optimization
    base_line_period = 26  # subject of optimization
    leading_spans_lookahead_period = 26  # subject of optimization
    leading_span_b_period = 52 # subject of optimization


    conversion_line_high = price_series.rolling(window=conversion_line_period).max()
    conversion_line_low = price_series.rolling(window=conversion_line_period).min()
    conversion_line = (conversion_line_high + conversion_line_low) / 2

    base_line_high = price_series.rolling(window=base_line_period).max()
    base_line_low = price_series.rolling(window=base_line_period).min()
    base_line = (base_line_high + base_line_low) / 2

    leading_span_a = ((conversion_line + base_line) / 2).shift(leading_spans_lookahead_period)
    leading_span_b = ((price_series.rolling(window=leading_span_b_period).max() + price_series.rolling(
        window=leading_span_b_period).min()) / 2).shift(leading_spans_lookahead_period)


    #
    # Rules calculation
    #

    # Cloud top and bottom series are defined using leading span A and B
    cloud_top = leading_span_a.rolling(1).max()
    cloud_bottom = leading_span_a.rolling(1).min()

    rule_price_above_cloud_top = price_series > cloud_top
    rule_price_below_cloud_bottom = price_series < cloud_bottom
    rule_price_in_cloud = (price_series < cloud_top) & (price_series > cloud_bottom)

    def get_regime(date):
        if date not in rule_price_above_cloud_top.index:
            logging.debug("Date not found at {0}".format(date))
            return None


        if rule_price_above_cloud_top[date]:
            return 1
        elif rule_price_below_cloud_bottom[date]:
            return -1
        elif rule_price_in_cloud[date]:
            return 0
        return None

    regime = get_regime(date.date())
    logging.debug("Ichi regime at {0}: {1}".format(date, regime))
    return regime


# Toolbox
def transactions_delta(trans_list):
    return sum([t.delta for t in trans_list])

def log_transactions(trans_list, msg):
    logging.debug(msg)
    [logging.debug(t) for t in trans_list]
    logging.debug('Transactions delta: {0}'.format(transactions_delta(trans_list)))

'''
New bullish zone position
'''


def new_position_bullish_zone(date, fut, opt_chain):
    """
    Returns transaction to open new Smart EXO position for bullish zone

    params date: current date
    params fut: current actual future contract
    params opt_chain: current actual options chain

    returns: List of Transactions to open
    """

    #
    # Opening hedged long ITM straddle in bullish zone
    #
    # https://files.slack.com/files-tmb/T0484J7T7-F2QBLK53R-93b4252806/pasted_image_at_2016_10_17_10_08_am_720.png

    trans_list = [
        # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
        Transaction(opt_chain[-2].c, date, 4.0, leg_name='bullish'),
        Transaction(opt_chain[-2].p, date, 2.0),
        Transaction(opt_chain[-9].p, date, -2.0),
        Transaction(opt_chain[9].c, date, -4.0),
    ]
    log_transactions(trans_list, 'New bullish zone position')
    return trans_list

'''
New bearish zone position
'''


def new_position_bearish_zone(date, fut, opt_chain):
    """
    Returns transaction to open new Smart EXO position for bearish zone

    params date: current date
    params fut: current actual future contract
    params opt_chain: current actual options chain

    returns: List of Transactions to open
    """

    #
    # Opening short butterfly in bearish zone
    #
    trans_list = [
        # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
        Transaction(opt_chain[-6].p, date, -1.0, leg_name='bearish'),
        Transaction(opt_chain[2].p, date, 1.0),

        Transaction(opt_chain[3].c, date, 1.0),
        Transaction(opt_chain[5].c, date, -1.0),
    ]

    log_transactions(trans_list, 'New bearish zone position')
    return trans_list

'''
New neutral zone position
'''


def new_position_neutral_zone(date, fut, opt_chain):
    """
    Returns transaction to open new Smart EXO position for neutral zone

    params date: current date
    params fut: current actual future contract
    params opt_chain: current actual options chain

    returns: List of Transactions to open
    """

    #
    # Opening long asymmetric butterfly in neutral zone
    #
    # https://files.slack.com/files-tmb/T0484J7T7-F2PGU8QNQ-6344e6a04c/pasted_image_at_2016_10_14_09_43_am_720.png
    trans_list = [
        # Transaction(asset, date, qty, price=[MktPrice], leg_name=['' or unique name])
        Transaction(opt_chain[-4].p, date, 1.0, leg_name='bearish'),
        Transaction(opt_chain[1].p, date, -2.0),

        Transaction(opt_chain[2].p, date, 1.0),
    ]
    log_transactions(trans_list, 'New neutral zone position')
    return trans_list

'''
Manage opened positions
'''
def manage_opened_position(date, fut, opt_chain, regime, opened_position):
    logging.debug('Current position delta: {0}'.format(opened_position.delta))

    # By default: do nothing
    return []


class SmartEXOIchiBullishStraddle150DeltaExpHedgedNov22_2016(ExoEngineBase):
    def __init__(self, symbol, direction, date, datasource, log_file_path=''):
        self._symbol = symbol
        super().__init__(symbol, direction, date, datasource, log_file_path=log_file_path)

    @staticmethod
    def direction_type():
        return 0

    @staticmethod
    def names_list(symbol):
        return ['{0}_{1}'.format(symbol, EXO_NAME)]

    @property
    def exo_name(self):
        return '{0}_{1}'.format(self._symbol, EXO_NAME)

    def is_rollover(self):
        if len(self.position) != 0:
            for p in self.position.legs.values():
                rh = RolloverHelper(p.instrument)
                if rh.is_rollover(p):
                    return True
        return False

    def process_rollover(self):
        trans_list = self.position.close_all_translist()
        logging.info('Rollover occured, new series used')
        return trans_list

    def process_day(self):
        """
        Main EXO's position management method
        :return: list of Transactions to process
        """

        # Get cont futures price for EXO
        exo_df, exo_info = self.datasource.exostorage.load_series("{0}_ContFut".format(self._symbol))

        regime = ichimoku_regimes(self.date, exo_df['exo'])

        trans_list = []

        if regime is None and len(self.position) > 0:
            return self.position.close_all_translist()

        instr = self.datasource.get(self._symbol, self.date)
        rh = RolloverHelper(instr)
        fut, opt_chain = rh.get_active_chains()

        if regime == 1 and 'bullish' not in self.position.legs:
            # Close all
            trans_list += self.position.close_all_translist()
            trans_list += new_position_bullish_zone(self.date, fut, opt_chain)

            return trans_list
        if regime == -1 and 'bearish' not in self.position.legs:
            # Close all
            trans_list += self.position.close_all_translist()
            trans_list += new_position_bearish_zone(self.date, fut, opt_chain)
            return trans_list

        if regime == 0 and 'neutral' not in self.position.legs:
            # Close all
            trans_list += self.position.close_all_translist()
            trans_list += new_position_neutral_zone(self.date, fut, opt_chain)
            return trans_list

        #
        # Manage opened position
        #
        return manage_opened_position(self.date, fut, opt_chain, regime, self.position)

