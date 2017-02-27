from exobuilder.contracts.futureschain import FuturesChain
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.tests.assetindexdict import AssetIndexDicts
from datetime import time as dttime
from datetime import datetime, date, timedelta
from exobuilder.contracts.instrument import Instrument
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.datasource_sql import DataSourceSQL
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.exostorage import EXOStorage
from exobuilder.exo.exoenginebase import ExoEngineBase
from exobuilder.exo.transaction import Transaction
import time


import logging
from exobuilder.algorithms.rollover_helper import RolloverHelper


class EXOContinuousFut(ExoEngineBase):
    ASSET_LIST = ['ES', 'CL', 'NG', 'ZN', 'ZS', 'ZW', 'ZC', '6E', 'CC']

    def __init__(self, symbol, direction, date, datasource, log_file_path=''):
        self._symbol = symbol

        super().__init__(symbol, direction, date, datasource, log_file_path=log_file_path)

    @staticmethod
    def direction_type():
        return 1


    @staticmethod
    def names_list(symbol):
        return [symbol + '_ContFut']

    @property
    def exo_name(self):
        return self._symbol + '_ContFut'

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
        instr = self.datasource.get(self._symbol, self.date)


        if len(self.position) == 0:
            instr = self.datasource.get(self._symbol, self.date)
            rh = RolloverHelper(instr)
            fut, opt_chain = rh.get_active_chains()
            if fut is None:
                if self.debug_mode:
                    self.logger.write(
                        'Futures contract or option chain not found.\n\tFuture: {0}\tOption chain: {1}\n'.format(
                            fut,
                            opt_chain
                        ))
                return []

            trans_list = [Transaction(fut, self.date, 1.0, fut.price, leg_name='fut')]
            return trans_list


    def as_dict(self):
        """
        Custom serialization logic for EXO
        :return:
        """
        exo_dict = super().as_dict()
        exo_dict['custom_class_name'] = 'EXOContinuousFut'
        return exo_dict





if __name__ == "__main__":
    try:
        from .settings import *
    except SystemError:
        from scripts.settings import *

    try:
        from .settings_local import *
    except SystemError:
        try:
            from scripts.settings_local import *
        except ImportError:
            pass
        pass


    mongo_db_name = 'tmldb'
    assetindex = AssetIndexMongo(MONGO_CONNSTR, mongo_db_name)
    exostorage = EXOStorage(MONGO_CONNSTR, mongo_db_name)

    base_date = datetime(2011, 3, 1, 10, 15, 0)

    futures_limit = 3
    options_limit = 10

    DEBUG = '.'

    datasource = DataSourceMongo(MONGO_CONNSTR, mongo_db_name, assetindex, futures_limit, options_limit, exostorage)

    server = 'h9ggwlagd1.database.windows.net'
    user = 'modelread'
    password = '4fSHRXwd4u'
    datasource = DataSourceSQL(server, user, password, assetindex, futures_limit, options_limit, exostorage)

    enddate = datetime.combine( datetime.now().date(), dttime(10, 15, 0))
    currdate = base_date

    #for i in range(100):
    while currdate <= enddate:
        start_time = time.time()
        #date = base_date + timedelta(days=i)
        date = currdate

        exo_engine = EXOContinuousFut('ES', 0, date, datasource, log_file_path=DEBUG)
        # Load EXO information from mongo
        exo_engine.load()
        exo_engine.calculate()
        end_time = time.time()
        print("{0} Elasped: {1}".format(date, end_time-start_time))

        currdate += timedelta(days=1)
    print('Done')
