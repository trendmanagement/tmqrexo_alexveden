from .assetindex import AssetIndexBase
import pymongo
from pymongo import MongoClient


class AssetIndexMongo(AssetIndexBase):
    def __init__(self, conn_str, dbname):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['tmldb']

    def get_instrument_info(self, symbol):
        """
        Returns underlying instrument information
        :param symbol: underlying ticker name
        :return: dict of underlying metadata
        """
        return self.db.instruments.find({'exchangesymbol': symbol}).next()

    def get_futures_list(self, date, instrument, limit):
        """
        Returns not expired futures contracts list on specific expiration
        :param date: datetime
        :param instrument: Instrument class instance to search
        :param limit: limit of expirations count
        :return: list of futures metadata dicts
        """
        fut_chains = []
        for contract in self.db.contracts.find({
            'idinstrument': instrument.dbid,
            'expirationdate': {'$gt': date}}).sort('expirationdate').limit(limit):
            fut_chains.append(contract)
        return fut_chains

    def get_options_list(self, date, futurecontract):
        opt_chains = []
        for contract in self.db.options.aggregate([
            {'$match': {'idcontract': futurecontract.dbid}},
            {'$sort': {'strikeprice': 1}},
            {'$group': {
                '_id': {'date': '$expirationdate'},
                'chain': {'$push': '$$ROOT'},
            }
            },
            {'$sort': {"_id.date": 1}}
        ]):
            opt_chains.append(contract)

        return opt_chains



