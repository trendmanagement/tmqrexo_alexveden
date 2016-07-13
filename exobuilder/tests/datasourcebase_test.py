import unittest
from .assetindexdict import AssetIndexDicts
from exobuilder.data.datasource import DataSourceBase
from exobuilder.contracts.instrument import Instrument
from datetime import datetime
import numpy as np

class DatasourceMongoTestCase(unittest.TestCase):
    def setUp(self):
        self.assetindex = AssetIndexDicts()
        self.date = datetime(2014, 1, 6, 10, 15, 0)
        futures_limit = 3
        options_limit = 10
        self.datasource = DataSourceBase(self.assetindex, self.date, futures_limit, options_limit)

    def test_constructor(self):
        self.assertEqual(self.datasource.assetindex, self.assetindex)
        self.assertEqual(self.datasource.date, self.date)
        self.assertEqual(self.datasource.futures_limit, 3)
        self.assertEqual(self.datasource.options_limit, 10)

    def test_get_item_as_instument(self):
        instr = self.datasource['EP']
        self.assertEqual(type(instr), Instrument)
        self.assertEqual(instr.name, 'EP')
        self.assertEqual(instr.date, self.date)
        self.assertEqual(instr.futures_limit, 3)
        self.assertEqual(instr.options_limit, 10)

    def test_get_notimplemented_abstract_methods(self):
        self.assertRaises(NotImplementedError, self.datasource.get_fut_data, None, None)
        self.assertRaises(NotImplementedError, self.datasource.get_option_data, None, None)
        self.assertRaises(NotImplementedError, self.datasource.get_extra_data, None, None)


