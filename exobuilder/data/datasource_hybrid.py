from .datasource import DataSourceBase
from datetime import datetime
import pymssql
from pymongo import MongoClient
import pymongo
from exobuilder.data.datasource_sql import DataSourceSQL

class DataSourceHybrid(DataSourceSQL):
    def __init__(self, server, user, password, assetindex, mongo_connstr, mongo_db, futures_limit, options_limit, exostorage=None):
        super().__init__(server, user, password, assetindex, futures_limit, options_limit, exostorage)

        self.client = MongoClient(mongo_connstr)
        self.db = self.client[mongo_db]


    def get_fut_data(self, dbid, date):
        try:
            return self.db['futurebarcol'].find({'bartime': {'$lte': date}, 'idcontract': dbid, 'errorbar': False}).sort('bartime', pymongo.DESCENDING).next()
        except:
            raise KeyError('Futures data not found contract id: {0} date: {1}'.format(dbid, date))
