import unittest
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.datasource_sql import DataSourceSQL
from datetime import datetime
import numpy as np

class DatasourceMongoTestCase(unittest.TestCase):
    def setUp(self):
        mongo_connstr = 'mongodb://localhost:27017/'
        mongo_db_name = 'tmldb'
        assetindex = AssetIndexMongo(mongo_connstr, mongo_db_name)
        self.date = datetime(2014, 1, 6, 10, 15, 0)
        futures_limit = 3
        options_limit = 10
        self.datasource = DataSourceMongo(mongo_connstr, mongo_db_name, assetindex, self.date, futures_limit, options_limit)

        server = 'h9ggwlagd1.database.windows.net'
        user = 'modelread'
        password = '4fSHRXwd4u'

        #self.datasource = DataSourceSQL(server, user, password, assetindex, futures_limit, options_limit)

    def test_data_source_get_fut_data_exists(self):
        dbid = 4736
        fut_data = self.datasource.get_fut_data(dbid, self.date)
        self.assertEqual(fut_data['close'], 1819.5)
        self.assertEqual(fut_data['datetime'], self.date)

    def test_data_source_get_fut_data_not_exists(self):
        dbid = 47380564654561560
        fut_data = (dbid, self.date)
        self.assertRaises(KeyError, self.datasource.get_fut_data, dbid, self.date)

    def test_data_source_get_extra_data_and_caching(self):
        self.assertEqual(0, len(self.datasource.extra_data_cache))
        rfr_data = self.datasource.get_extra_data('riskfreerate', self.date)
        self.assertEqual(0.265, rfr_data)
        # Get from cache
        rfr_data = self.datasource.get_extra_data('riskfreerate', self.date)
        self.assertEqual(0.265, rfr_data)
        self.assertNotEqual(0, len(self.datasource.extra_data_cache))
        self.assertTrue('riskfreerate' in self.datasource.extra_data_cache)
        self.assertEqual(0.265, self.datasource.extra_data_cache['riskfreerate'][self.date])

    def test_data_source_get_extra_data_different_dates(self):
        rfr_data = self.datasource.get_extra_data('riskfreerate', self.date)
        rfr_data = self.datasource.get_extra_data('riskfreerate', datetime(2014, 1, 25, 10, 15, 0))

        self.assertEqual(0.26, rfr_data)
        self.assertNotEqual(2, len(self.datasource.extra_data_cache))
        self.assertTrue('riskfreerate' in self.datasource.extra_data_cache)
        self.assertEqual(0.26, self.datasource.extra_data_cache['riskfreerate'][datetime(2014, 1, 25, 10, 15, 0)])

    def test_data_source_get_extra_data_raise_on_wrongkey(self):
        self.assertRaises(KeyError, self.datasource.get_extra_data, 'noexitsdfsdfsf', self.date)

    def test_data_source_get_option_data_prev_day_price(self):
        opt_dbid = 11488838
        opt_data = self.datasource.get_option_data(opt_dbid, datetime(2013, 8, 28, 10, 15, 0))

        self.assertEqual(opt_data['impliedvol'], 0.12517)
        #
        # !!! Returns previous day IV (calculated on settlement)
        #
        self.assertEqual(opt_data['datetime'], datetime(2013, 8, 27, 0, 0, 0))

    def test_data_source_get_option_data_not_exists(self):
        dbid = 11488838
        self.assertRaises(KeyError, self.datasource.get_option_data, dbid, datetime(1900, 8, 28, 10, 15, 0))

