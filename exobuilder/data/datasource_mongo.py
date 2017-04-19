from .datasource import DataSourceBase
from .exceptions import QuoteNotFoundException
from pymongo import MongoClient
import pymongo
from datetime import datetime


class DataSourceMongo(DataSourceBase):
    def __init__(self, conn_str, dbname, assetindex, futures_limit, options_limit, exostorage=None):
        super().__init__(assetindex, futures_limit, options_limit, exostorage=exostorage)
        self.client = MongoClient(conn_str)
        self.db = self.client[dbname]

        # Creating indexes for fast data fetching
        self.db.futures_data.create_index([('idcontract', pymongo.ASCENDING), ('datetime', pymongo.ASCENDING)])

        # Extradata cache
        self.extra_data_cache = {}

    def _shrink_datetime(self, dt):
        return datetime.combine(
            dt.date(),
            datetime.min.time())

    def get_fut_data(self, dbid, date):
        try:
            return self.db.contracts_bars.find({'datetime': {'$lte': date}, 'idcontract': dbid}).next()
        except StopIteration:
            raise QuoteNotFoundException('Futures data not found contract id: {0} date: {1}'.format(dbid, date))

    def get_fut_settlement(self, dbid, date):


        try:
            return self.db['futures_contract_settlements'].find(
                {'date': self._shrink_datetime(date), 'idcontract': dbid}).next()['settlement']
        except StopIteration:
            raise QuoteNotFoundException(
                'Futures settlement data not found contract id: {0} date: {1}'.format(dbid, self._shrink_datetime(date)))

    def get_extra_data(self, key, date):

        if key == 'riskfreerate':
            if key in self.extra_data_cache:
                if date in self.extra_data_cache[key]:
                    return self.extra_data_cache[key][date]

            rfr_dic = self.extra_data_cache.setdefault(key, {})
            #
            #  Getting risk-free-rate on previous day
            #
            try:
                rfr_result = self.db['option_input_data'].find({
                    "idoptioninputsymbol": 15,
                    "optioninputdatetime": {
                        '$lt': self._shrink_datetime(date)}
                }).sort([("optioninputdatetime", -1)]).limit(1).next()

                rfr_dic[date] = rfr_result["optioninputclose"] / 100.0
                return self.extra_data_cache[key][date]
            except StopIteration:
                return 0.0
        else:
            raise KeyError("Unknown key for extra_data, only 'riskfreerate' supported.")

    def get_option_data(self, dbid, date):
        #
        # Returning previous day IV information
        #
        try:
            return self.db.options_data.find({
                'idoption': dbid,
                'datetime': {'$lt': self._shrink_datetime(date)}
            }).sort([('datetime', -1)]).limit(1).next()
        except StopIteration:
            raise QuoteNotFoundException('Option data not found contract id: {0} date: {1}'.format(dbid, date))

    def get_option_settlement(self, dbid, date):
        try:
            return self.db.options_data.find({
                'idoption': dbid,
                'datetime': self._shrink_datetime(date),
            }).sort([('datetime', -1)]).limit(1).next()['price']
        except StopIteration:
            raise QuoteNotFoundException(
                'Option settlement data not found contract id: {0} date: {1}'.format(dbid, date))
