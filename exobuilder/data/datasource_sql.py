from .datasource import DataSourceBase
from .exceptions import QuoteNotFoundException
from datetime import datetime
import pymssql


class DataSourceSQL(DataSourceBase):
    def __init__(self, server, user, password, assetindex, futures_limit, options_limit, exostorage=None):
        raise NotImplementedError("Please switch to DatasourceMongo")



