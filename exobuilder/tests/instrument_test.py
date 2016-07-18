import unittest
from exobuilder.contracts.instrument import Instrument
from exobuilder.contracts.futureschain import FuturesChain
from .assetindexdict import AssetIndexDicts
from .datasourcefortest import DataSourceForTest
from datetime import datetime

class InstrumentCase(unittest.TestCase):
    def setUp(self):
        self.assetindex = AssetIndexDicts()

        self.symbol = 'EP'
        self.date = datetime(2014, 1, 5, 0, 0, 0)
        self.futures_limit = 12
        self.instrument_dbid = 11
        self.datasource = DataSourceForTest(self.assetindex, self.date, self.futures_limit, 0)
        self.instrument = self.datasource[self.symbol]
        return

    def test_instrument_constructor(self):
        instrument = self.instrument
        self.assertEqual(type(dict()), type(instrument._datadic))
        self.assertEqual(type(self.assetindex), type(instrument.datasource.assetindex))
        self.assertEqual(type(self.datasource), type(instrument.datasource))

    def test_instrument_has_name(self):
        instrument = self.instrument
        self.assertEqual(self.symbol, instrument.name)

    def test_instrument_has_symbol(self):
        instrument = self.instrument
        self.assertEqual(self.symbol, instrument.symbol)

    def test_instrument_has_date(self):
        instrument = self.instrument
        self.assertEqual(self.date, instrument.date)

    def test_instrument_has_futures_limit(self):
        instrument = self.instrument
        self.assertEqual(self.futures_limit, instrument.futures_limit)

    def test_instrument_has_options_limit(self):
        instrument = self.instrument
        self.assertEqual(0, instrument.options_limit)

    def test_instrument_has_dbid(self):
        instrument = self.instrument
        self.assertEqual(self.instrument_dbid, instrument.dbid)

    def test_instrument_has_futures_and_caching(self):
        chain = self.instrument.futures
        self.assertEqual(type(chain), FuturesChain)
        # Chain caching
        self.assertEqual(chain, self.instrument.futures)

    def test_instrument_has_futures_point_value(self):
        self.assertEqual(self.instrument.point_value_futures, 1.0 / 0.25 * 12.5)

    def test_instrument_has_options_point_value(self):
        inst = self.datasource[self.symbol]
        inst._datadic['optiontickvalue'] = 25.0
        inst._datadic['optionticksize'] = .5
        self.assertEqual(self.instrument.point_value_options, 1.0 / 0.5 * 25.0)



if __name__ == '__main__':
    unittest.main()
