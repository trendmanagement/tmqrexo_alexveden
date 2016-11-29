import unittest
from exobuilder.contracts.futureschain import FuturesChain
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.tests.assetindexdict import AssetIndexDicts
from datetime import datetime, date, timedelta, time as dttime
from exobuilder.contracts.instrument import Instrument
from exobuilder.data.datasource_mongo import DataSourceMongo
from exobuilder.data.datasource_sql import DataSourceSQL
from exobuilder.data.assetindex_mongo import AssetIndexMongo
from exobuilder.data.exostorage import EXOStorage
from exobuilder.exo.exoenginebase import ExoEngineBase
from exobuilder.exo.transaction import Transaction
import time
from exobuilder.algorithms.rollover_helper import RolloverHelper

import importlib


from scripts.settings import *

from backtester.reports.payoffs import PayoffAnalyzer


class PayoffsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        mongo_connstr = 'mongodb://exowriter:qmWSy4K3@10.0.1.2/tmldb?authMechanism=SCRAM-SHA-1'
        mongo_db_name = 'tmldb'
        assetindex = AssetIndexMongo(mongo_connstr, mongo_db_name)
        exostorage = EXOStorage(mongo_connstr, mongo_db_name)

        # base_date = datetime(2011, 6, 13, 12, 45, 0)

        futures_limit = 3
        options_limit = 10


        server = 'h9ggwlagd1.database.windows.net'
        user = 'modelread'
        password = '4fSHRXwd4u'
        self.datasource = DataSourceSQL(server, user, password, assetindex, futures_limit, options_limit, exostorage)

    def test_calcpayoff(self):
        payoff = PayoffAnalyzer(self.datasource)

        payoff.load_exo('ES_BullishCollarBW')

        payoff.calc_payoff(strikes_to_analyze=10)


        self.assertEqual(True, False)

    def test_position_info(self):
        payoff = PayoffAnalyzer(self.datasource)

        payoff.load_exo('ES_BullishCollarBW')

        pos_info = payoff.position_info()

        self.assertEqual(True, False)

    def test_campaign(self):
        CAMPAIGN_NAME = 'CL_Bidirectional'
        strikes_on_graph = 50

        payoff = PayoffAnalyzer(self.datasource)
        analysis_date = None

        # Edit (or comment) next line to change analysis date
        analysis_date = datetime(2016, 11, 18, 23, 59)

        payoff.load_campaign(CAMPAIGN_NAME, date=analysis_date)

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
