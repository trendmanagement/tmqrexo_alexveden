import unittest
from exobuilder.exo.exoenginebase import ExoEngineBase
from .assetindexdict import AssetIndexDicts
from datetime import datetime, date
from exobuilder.contracts.instrument import Instrument
from .datasourcefortest import DataSourceForTest
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.exo.transaction import Transaction
from exobuilder.exo.position import Position
from .assetindexdict import AssetIndexDicts
from .datasourcefortest import DataSourceForTest


class ExoEngineBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.assetindex = AssetIndexDicts()
        self.symbol = 'EP'
        self.date = datetime(2014, 1, 5, 0, 0, 0)
        self.futures_limit = 12
        self.instrument_dbid = 11
        self.datasource = DataSourceForTest(self.assetindex, self.date, self.futures_limit, 0)
        self.instrument = self.datasource[self.symbol]

        self.contract_dict = {'_id': '577a4fa34b01f47f84cab23c',
                              'contractname': 'F.EPZ16',
                              'cqgsymbol': 'F.EPZ16',
                              'expirationdate': datetime(2016, 12, 16, 0, 0),
                              'idcontract': 6570,
                              'idinstrument': 11,
                              'month': 'Z',
                              'monthint': 12,
                              'year': 2016}
        self.fut_contract = FutureContract(self.contract_dict, self.instrument)
        self.trans = Transaction(self.fut_contract, self.date, 4.0, 12.3)
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



