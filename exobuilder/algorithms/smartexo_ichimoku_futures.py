import time
from datetime import datetime, timedelta, time as dttime

from exobuilder.algorithms.rollover_helper import RolloverHelper
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.datasource_sql import DataSourceSQL
from exobuilder.data.exostorage import EXOStorage
from exobuilder.exo.exoenginebase import ExoEngineBase
from exobuilder.exo.transaction import Transaction


class SmartEXOichimokuFutures(ExoEngineBase):
    def __init__(self, symbol, direction, date, datasource, log_file_path=''):
        self._direction = direction
        self._symbol = symbol

        if self._direction != 1 and self._direction != -1:
            raise ValueError('self._direction != 1 and self._direction != -1')

        super().__init__(symbol, direction, date, datasource, log_file_path=log_file_path)

    @staticmethod
    def direction_type():
        return 0

    @staticmethod
    def names_list(symbol):
        return [symbol + '_SMART_Ichimoku_Long', symbol + '_SMART_Ichimoku_Short']

    @property
    def exo_name(self):
        if self._direction == 1:
            return self._symbol + '_SMART_Ichimoku_Long'
        elif self._direction == -1:
            return self._symbol + '_SMART_Ichimoku_Short'

    def is_rollover(self):
        if len(self.position) != 0:
            for p in self.position.legs.values():
                rh = RolloverHelper(p.instrument)
                if rh.is_rollover(p):
                    return True
        return False

    def process_rollover(self):
        trans_list = self.position.close_all_translist()
        return trans_list

    def ichimoku_regimes(self, price_df):

        conversion_line_period = 9 # subject of optimization
        conversion_line_high = price_df.rolling(window=conversion_line_period).max()
        conversion_line_low = price_df.rolling(window=conversion_line_period).min()
        conversion_line = (conversion_line_high + conversion_line_low) / 2

        base_line_period = 26  # subject of optimization
        base_line_high = price_df.rolling(window=base_line_period).max()
        base_line_low = price_df.rolling(window=base_line_period).min()
        base_line = (base_line_high + base_line_low) / 2

        leading_spans_lookahead_period = 26  # subject of optimization
        leading_span_a = ((conversion_line + base_line) / 2).shift(leading_spans_lookahead_period)

        leading_span_b_period = 52 # subject of optimization
        leading_span_b = ((price_df.rolling(window=leading_span_b_period).max() + price_df.rolling(
            window=leading_span_b_period).min()) / 2).shift(leading_spans_lookahead_period)


        #
        # Rules calculation
        #

        # Cloud top and bottom series are defined using leading span A and B
        cloud_top = leading_span_a.rolling(1).max()
        cloud_bottom = leading_span_a.rolling(1).min()

        rule_price_above_cloud_top = price_df > cloud_top
        rule_price_below_cloud_bottom = price_df < cloud_bottom
        rule_price_in_cloud = (price_df < cloud_top) & (price_df > cloud_bottom)

        def get_regime(date):
            if date not in rule_price_above_cloud_top.index:
                self.logger.write("Date not found at {0} for {1}\n".format(date, self._symbol))
                return None


            if rule_price_above_cloud_top[date]:
                return 1
            elif rule_price_below_cloud_bottom[date]:
                return -1
            elif rule_price_in_cloud[date]:
                return 0
            return None

        regime = get_regime(self.date.date())
        self.logger.write("Ichi regime at {0}: {1}\n".format(self.date, regime))
        return regime


    def process_day(self):
        """
        Main EXO's position management method
        :return: list of Transactions to process
        """

        # Get cont futures price for EXO
        exo_df, exo_info = self.datasource.exostorage.load_series("{0}_ContFut".format(self._symbol))

        regime = self.ichimoku_regimes(exo_df['exo'])

        trans_list = []

        if regime is None and len(self.position) > 0:
            return self.position.close_all_translist()

        if regime == 1 and 'bullish' not in self.position.legs:
            # Close all
            trans_list += self.position.close_all_translist()

            instr = self.datasource.get(self._symbol, self.date)
            rh = RolloverHelper(instr)
            fut, opt_chain = rh.get_active_chains()

            trans_list += [
                    Transaction(fut, self.date, 15.0, fut.price, leg_name='bullish'),
            ]
            return trans_list
        if regime == -1 and 'bearish' not in self.position.legs:
            # Close all
            trans_list += self.position.close_all_translist()

            instr = self.datasource.get(self._symbol, self.date)
            rh = RolloverHelper(instr)
            fut, opt_chain = rh.get_active_chains()

            trans_list += [
                Transaction(fut, self.date, 1.0, fut.price, leg_name='bearish'),
            ]
            return trans_list

        if regime == 0 and 'neutral' not in self.position.legs:
            # Close all
            trans_list += self.position.close_all_translist()

            instr = self.datasource.get(self._symbol, self.date)
            rh = RolloverHelper(instr)
            fut, opt_chain = rh.get_active_chains()

            trans_list += [
                Transaction(fut, self.date, 5.0, fut.price, leg_name='neutral'),
            ]
            return trans_list

        return []



