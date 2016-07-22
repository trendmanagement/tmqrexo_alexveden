from exobuilder.contracts.futureschain import FuturesChain
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.tests.assetindexdict import AssetIndexDicts
from datetime import datetime, date
from exobuilder.contracts.instrument import Instrument
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.exostorage import EXOStorage
from exobuilder.exo.exoenginebase import ExoEngineBase
from exobuilder.exo.transaction import Transaction

class EXOContinuousFut(ExoEngineBase):
    def __init__(self, symbol, date, datasource):
        super().__init__(symbol, date, datasource)

        self._exosuffix = '_ContFut'

    def is_rollover(self):
        pass

    def process_rollover(self):
        """
        Typically we should only close old position on rollover day
        :return:
        """
        pass

    def process_day(self):
        """
        Main EXO's position management method
        :return: list of Transactions to process
        """
        if len(self.position) == 0:
            instr = self.datasource[self._symbol]
            fut = instr.futures[0]
            return [Transaction(fut, self.date, 1.0, fut.price)]

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

    date = datetime(2014, 1, 7, 10, 15, 0)
    futures_limit = 3
    options_limit = 10

    datasource = DataSourceMongo(mongo_connstr, mongo_db_name, assetindex, date, futures_limit, options_limit,
                                 exostorage)

    exo_engine = EXOContinuousFut('ES', date, datasource)
    exo_engine.load()
    exo_engine.calculate()
    print('Done')
