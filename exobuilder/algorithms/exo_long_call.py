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

import logging

class EXOBullishCall(ExoEngineBase):
    def __init__(self, symbol,  direction, date, datasource, log_file_path=''):
        self._symbol = symbol

        super().__init__(symbol, direction, date, datasource, log_file_path=log_file_path)

    @staticmethod
    def direction_type():
        return 1

    @property
    def exo_name(self):
        return self._symbol + '_BullishCall'

    def is_rollover(self):
        if len(self.position) != 0:

            opt = self.position.legs['opt_call']
            if opt.to_expiration_days <= 2:
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
            fut = instr.futures[0]
            if fut.to_expiration_days <= 2:
                fut = instr.futures[1]

            opt_chain = fut.options[0]
            if opt_chain.to_expiration_days <= 2:
                opt_chain = fut.options[1]

            call = opt_chain[0].C

            trans_list = [
                Transaction(call, self.date, 1.0, call.price, leg_name='opt_call'),
            ]
            return trans_list



if __name__ == "__main__":
    mongo_connstr = 'mongodb://localhost:27017/'
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

    # for i in range(100):
    while currdate <= enddate:
        start_time = time.time()
        # date = base_date + timedelta(days=i)
        date = currdate

        exo_engine = EXOBullishCall('ES',0, date, datasource, log_file_path=DEBUG)
        # Load EXO information from mongo
        exo_engine.load()
        exo_engine.calculate()
        end_time = time.time()

        currdate += timedelta(days=1)
        print("{0} Elapsed: {1}".format(date, end_time-start_time))
    print('Done')
