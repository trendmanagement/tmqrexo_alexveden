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


class EXOVerticalSpread(ExoEngineBase):
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
        return [symbol + '_CallSpread', symbol + '_PutSpread']

    @property
    def exo_name(self):
        if self._direction == 1:
            return self._symbol + '_CallSpread'
        elif self._direction == -1:
            return self._symbol + '_PutSpread'

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


    def process_day(self):
        """
        Main EXO's position management method
        :return: list of Transactions to process
        """


        if len(self.position) == 0:
            instr = self.datasource.get(self._symbol, self.date)
            rh = RolloverHelper(instr)
            fut, opt_chain = rh.get_active_chains()
            if fut is None or opt_chain is None:
                if self.debug_mode:
                    self.logger.write(
                        'Futures contract or option chain not found.\n\tFuture: {0}\tOption chain: {1}\n'.format(
                            fut,
                            opt_chain
                        ))
                return []

            if self._direction == 1:
                itm_call = opt_chain[-2].C
                otm_call = opt_chain[10].C

                return [
                    Transaction(itm_call, self.date, 1.0, itm_call.price, leg_name='opt_itm_leg'),
                    Transaction(otm_call, self.date, -1.0, otm_call.price, leg_name='opt_otm_leg'),
                ]
            if self._direction == -1:
                itm_put = opt_chain[2].P
                otm_put = opt_chain[-10].P

                return [
                    Transaction(itm_put, self.date, 1.0, itm_put.price, leg_name='opt_itm_leg'),
                    Transaction(otm_put, self.date, -1.0, otm_put.price, leg_name='opt_otm_leg'),
                ]




if __name__ == "__main__":
    mongo_connstr = 'mongodb://exowriter:qmWSy4K3@10.0.1.2/tmldb?authMechanism=SCRAM-SHA-1'
    mongo_db_name = 'tmldb'
    assetindex = AssetIndexMongo(mongo_connstr, mongo_db_name)
    exostorage = EXOStorage(mongo_connstr, mongo_db_name)

    base_date = datetime(2014, 1, 13, 12, 45, 0)
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

    instruments = ['CL', 'ES']
    directions = [1, -1]

    # for i in range(100):
    while currdate <= enddate:
        start_time = time.time()
        # date = base_date + timedelta(days=i)
        date = currdate

        for ticker in instruments:
            for dir in directions:
                with EXOVerticalSpread(ticker, dir, date, datasource, log_file_path=DEBUG) as exo_engine:
                    # Load EXO information from mongo
                    exo_engine.load()
                    exo_engine.calculate()


        end_time = time.time()

        currdate += timedelta(days=1)
        print("{0} Elasped: {1}".format(date, end_time-start_time))
    print('Done')
