import pymongo
from pymongo import MongoClient

from exobuilder.data.datasource_mongo import DataSourceMongo
from .exceptions import QuoteNotFoundException


class DataSourceHybrid(DataSourceMongo):
    def __init__(self, mongo_connstr, mongo_db, assetindex, online_mongo_connstr, online_mongo_db, futures_limit, options_limit, exostorage=None):
        super().__init__(mongo_connstr, mongo_db, assetindex, futures_limit, options_limit, exostorage)

        self.online_client = MongoClient(online_mongo_connstr)
        self.online_db = self.online_client[online_mongo_db]


    def get_fut_data(self, dbid, date):
        try:
            return self.online_db['futurebarcol'].find({'bartime': {'$lte': date}, 'idcontract': dbid, 'errorbar': False}).sort('bartime', pymongo.DESCENDING).next()
        except:
            raise QuoteNotFoundException('Futures data not found contract id: {0} date: {1}'.format(dbid, date))
