from .datasource import DataSourceBase
from pymongo import MongoClient
import pymongo
from datetime import datetime

class DataSourceMongo(DataSourceBase):
    def __init__(self, conn_str, dbname, assetindex, date, futures_limit, options_limit):
        super().__init__(assetindex, date, futures_limit, options_limit)
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['tmldb']

        # Creating indexes for fast data fetching
        self.db.futures_data.create_index([('idcontract', pymongo.ASCENDING),('datetime', pymongo.ASCENDING)])

        # Extradata cache
        self.extra_data_cache = {}

    def _shrink_datetime(self, dt):
        return datetime.combine(
            dt.date(),
            datetime.min.time())


    def get_fut_data(self, dbid, date):
        try:
            return self.db.futures_data.find({'datetime': date, 'idcontract': dbid}).next()
        except:
            return {'datetime': date, 'close': float('nan')}

    def get_extra_data(self, key, date):


        if key == 'riskfreerate':
            if key in self.extra_data_cache:
                if date in self.extra_data_cache[key]:
                    return self.extra_data_cache[key][date]

            rfr_dic = self.extra_data_cache.setdefault(key, {})
            #
            #  Getting risk-free-rate on previous day
            #
            rfr_result = self.db.options_data_inputs.find({"idoptioninputsymbol": 15,
                                              "optioninputdatetime": { '$lt': self._shrink_datetime(date)}
                                              }).sort([("optioninputdatetime", -1)]).limit(1).next()

            rfr_dic[date] = rfr_result["optioninputclose"]
            return self.extra_data_cache[key][date]
        else:
            raise KeyError("Unknown key for extra_data, only 'riskfreerate' supported.")

    def get_option_data(self, dbid, date):
        #
        # Returning previous day IV information
        #
        return self.db.options_data.find({'idoption': dbid,
                                          'datetime': {'$lt': self._shrink_datetime(date)}
                                          }).sort([('datetime', -1)]).limit(1).next()

