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

            if rule_price_above_cloud_top[date]:
                return 1,
            elif rule_price_below_cloud_bottom[date]:
                return -1
            elif rule_price_in_cloud[date]:
                return 0
            return None

        regime = get_regime(self.date)
        self.logger.write("Ichi regime at {0}: {1}".format(regime, regime))
        return regime


    def process_day(self):
        """
        Main EXO's position management method
        :return: list of Transactions to process
        """

        # Get cont futures price for EXO
        exo_df, exo_info = self.datasource.exostorage.load_series("{0}_ContFut".format(self._symbol))

        regime = self.ichimoku_regimes(exo_df['exo'], self.date)

        trans_list = []

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




if __name__ == "__main__":
    mongo_connstr = 'mongodb://exowriter:qmWSy4K3@10.0.1.2/tmldb?authMechanism=SCRAM-SHA-1'
    mongo_db_name = 'tmldb'
    assetindex = AssetIndexMongo(mongo_connstr, mongo_db_name)
    exostorage = EXOStorage(mongo_connstr, mongo_db_name)

    base_date = datetime(2011, 6, 13, 12, 45, 0)
    futures_limit = 3
    options_limit = 10

    DEBUG = '.'

    datasource = DataSourceMongo(mongo_connstr, mongo_db_name, assetindex, futures_limit, options_limit, exostorage)

    server = 'h9ggwlagd1.database.windows.net'
    user = 'modelread'
    password = '4fSHRXwd4u'
    datasource = DataSourceSQL(server, user, password, assetindex, futures_limit, options_limit, exostorage)

    enddate = datetime.combine(datetime.now().date(), dttime(12, 45, 0))
    currdate = base_date

    instruments = ['CL', 'ES', 'NG', 'ZC', 'ZS', 'ZW', 'ZN']
    directions = [1, -1]

    # for i in range(100):
    while currdate <= enddate:
        start_time = time.time()
        # date = base_date + timedelta(days=i)
        date = currdate

        for ticker in instruments:
            asset_info = assetindex.get_instrument_info(ticker)
            exec_time_end, decision_time_end = AssetIndexMongo.get_exec_time(date, asset_info)

            for dir in directions:
                with SmartEXOichimokuFutures(ticker, dir, date, datasource,log_file_path=DEBUG) as exo_engine:
                    # Load EXO information from mongo
                    exo_engine.load()
                    exo_engine.calculate()


        end_time = time.time()

        currdate += timedelta(days=1)
        print("{0} Elasped: {1}".format(date, end_time-start_time))
    print('Done')
