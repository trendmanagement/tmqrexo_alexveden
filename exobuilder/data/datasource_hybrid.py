import pymongo
from pymongo import MongoClient

from exobuilder.data.datasource_mongo import DataSourceMongo
from .exceptions import QuoteNotFoundException


class DataSourceHybrid(DataSourceMongo):
    def __init__(self, mongo_connstr, mongo_db, assetindex, online_mongo_connstr, online_mongo_db, futures_limit, options_limit, exostorage=None):
        raise Exception("This datasource type is obsolete please switch to DataSourceMongo")
