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
import pandas as pd
import numpy as np
import pickle

class EXOTestEngine(ExoEngineBase):
    @property
    def exo_name(self):
        return '_EXOTEST'


class ExoEngineBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.assetindex = AssetIndexDicts()
        self.symbol = 'EP'
        self.date = datetime(2014, 1, 5, 0, 0, 0)
        self.futures_limit = 12
        self.instrument_dbid = 11
        self.datasource = DataSourceForTest(self.assetindex, self.futures_limit, 0)
        self.instrument = self.datasource.get(self.symbol, self.date)

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
        self.exo_engine = EXOTestEngine(self.date, self.datasource)

    def test_constructor(self):
        exo_engine = ExoEngineBase(self.date, self.datasource)

        self.assertEqual(exo_engine._date, self.date)
        self.assertEqual(exo_engine._datasource, self.datasource)
        self.assertEqual(True, isinstance(exo_engine._position, Position))

    def test_has_date(self):
        self.assertEqual(self.exo_engine.date, self.date)

    def test_has_datasource(self):
        self.assertEqual(self.exo_engine.datasource, self.datasource)

    def test_has_position(self):
        self.assertEqual(True, isinstance(self.exo_engine.position, Position))


    def test_has_series(self):
        self.assertTrue(isinstance(self.exo_engine.series, pd.DataFrame))

    def test_has_exo_name_and_raises(self):
        exo_engine = ExoEngineBase(self.date, self.datasource)

        def name_raises():
            exo_engine.name

        def exo_name_raises():
            exo_engine.exo_name

        self.assertRaises(NotImplementedError, name_raises)
        self.assertRaises(NotImplementedError, exo_name_raises)

    def test_has_process_day_raises(self):
        exo_engine = ExoEngineBase(self.date, self.datasource)
        self.assertRaises(NotImplementedError, exo_engine.process_day)
        self.assertRaises(NotImplementedError, exo_engine.process_rollover)
        self.assertRaises(NotImplementedError, exo_engine.is_rollover)


    def test_as_dict(self):
        exo_engine = EXOTestEngine(self.date, self.datasource)
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3)
        exo_engine.position.add(trans)

        tr_list = exo_engine._transactions
        tr_list.append(trans)

        date = pd.date_range("2015-01-01 00:00:00", "2015-01-01 00:00:10", freq="1S")
        price = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=np.float64)

        exo_engine._series = pd.DataFrame(price, index=date, columns=['exo'])
        exo_engine._series.index = pd.to_datetime(exo_engine._series.index)


        exo_dic = exo_engine.as_dict()

        self.assertEqual(True, 'position' in exo_dic)
        self.assertEqual(exo_engine.position.as_dict(), exo_dic['position'])

        self.assertEqual(True, 'transactions' in exo_dic)
        self.assertEqual([trans.as_dict()], exo_dic['transactions'])

        self.assertEqual(exo_dic['name'], self.exo_engine.name)

        self.assertEqual(True, 'series' in exo_dic)
        self.assertEqual(pickle.dumps(exo_engine.series), exo_dic['series'])




