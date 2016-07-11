from .datasource import DataSourceBase
from pymongo import MongoClient
import pymongo

class DataSourceMongo(DataSourceBase):
    def __init__(self, conn_str, dbname, assetindex, date, futures_limit, options_limit):
        super().__init__(assetindex, date, futures_limit, options_limit)
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['tmldb']

        # Creating indexes for fast data fetching
        self.db.futures_data.create_index([('idcontract', pymongo.ASCENDING),('datetime', pymongo.ASCENDING)])


    def get_fut_data(self, dbid, date):
        try:
            return self.db.futures_data.find({'datetime': date, 'idcontract': dbid}).next()
        except:
            return {'close': float('nan')}
