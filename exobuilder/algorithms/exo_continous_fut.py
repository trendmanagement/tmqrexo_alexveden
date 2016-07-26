from exobuilder.contracts.futureschain import FuturesChain
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.tests.assetindexdict import AssetIndexDicts
from datetime import datetime, date, timedelta
from exobuilder.contracts.instrument import Instrument
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.datasource_sql import DataSourceSQL
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.exostorage import EXOStorage
from exobuilder.exo.exoenginebase import ExoEngineBase
from exobuilder.exo.transaction import Transaction
import time

class EXOContinuousFut(ExoEngineBase):
    def __init__(self, symbol, date, datasource):
        super().__init__(date, datasource)
        self._symbol = symbol

    @property
    def exo_name(self):
        return self._symbol + '_ContFut'

    def is_rollover(self):
        if len(self.position) != 0:
            fut = self.position.legs['fut']
            if fut.to_expiration_days <= 2:
                return True

        return False

    def process_rollover(self):
        return self.position.close_all_translist()

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

            return [Transaction(fut, self.date, 1.0, fut.price, leg_name='fut')]

    def as_dict(self):
        """
        Custom serialization logic for EXO
        :return:
        """
        exo_dict = super().as_dict()
        exo_dict['custom_class_name'] = 'EXOContinuousFut'
        return exo_dict





if __name__ == "__main__":
    mongo_connstr = 'mongodb://localhost:27017/'
    mongo_db_name = 'tmldb'
    assetindex = AssetIndexMongo(mongo_connstr, mongo_db_name)
    exostorage = EXOStorage(mongo_connstr, mongo_db_name)

    base_date = datetime(2014, 1, 13, 10, 15, 0)
    futures_limit = 3
    options_limit = 10

    datasource = DataSourceMongo(mongo_connstr, mongo_db_name, assetindex, futures_limit, options_limit, exostorage)

    server = 'h9ggwlagd1.database.windows.net'
    user = 'modelread'
    password = '4fSHRXwd4u'
    datasource = DataSourceSQL(server, user, password, assetindex, futures_limit, options_limit, exostorage)

    for i in range(100):
        start_time = time.time()
        date = base_date + timedelta(days=i)

        exo_engine = EXOContinuousFut('ES', date, datasource)
        # Load EXO information from mongo
        exo_engine.load()
        exo_engine.calculate()
        end_time = time.time()
        print("{0} Elasped: {1}".format(date, end_time-start_time))
    print('Done')
