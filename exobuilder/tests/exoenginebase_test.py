import unittest
from exobuilder.exo.exoenginebase import ExoEngineBase
from .assetindexdict import AssetIndexDicts
from datetime import datetime, date
from exobuilder.contracts.instrument import Instrument
from .datasourcefortest import DataSourceForTest

class ExoEngineBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.assetindex = AssetIndexDicts()
        self.symbol = 'EP'
        self.date = datetime(2014, 1, 5, 0, 0, 0)
        self.futures_limit = 12
        self.datasource = DataSourceForTest(self.assetindex, self.date, self.futures_limit, 0)
        self.instrument = self.datasource[self.symbol]
        self.exo_engine = ExoEngineBase(self.date, self.datasource)

    def test_constructor(self):
        exo_engine = ExoEngineBase(self.date, self.datasource)

        self.assertEqual(exo_engine._date, self.date)
        self.assertEqual(exo_engine._datasource, self.datasource)
        self.assertEqual(exo_engine._positions, [])

    def test_has_date(self):
        self.assertEqual(self.exo_engine.date, self.date)

    def test_has_datasource(self):
        self.assertEqual(self.exo_engine.datasource, self.datasource)




if __name__ == '__main__':
    unittest.main()
