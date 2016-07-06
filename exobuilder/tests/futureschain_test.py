import unittest
from exobuilder.contracts.futureschain import FuturesChain
from exobuilder.contracts.futurecontract import FutureContract
from .assetindexdict import AssetIndexDicts
from datetime import datetime, date
from exobuilder.contracts.instrument import Instrument

class FuturesChainTestCase(unittest.TestCase):
    def setUp(self):
        self.assetindex = AssetIndexDicts()
        self.symbol = 'EP'
        self.date = datetime(2014, 1, 5, 0, 0, 0)
        self.futures_limit = 12
        self.instrument = Instrument(self.symbol, self.date, self.futures_limit, self.assetindex)
        self.fut_chain = FuturesChain(self.instrument)

    def test_constructor(self):
        fut_chain = FuturesChain(self.instrument)
        self.assertEqual(fut_chain.instrument, self.instrument)

    def test_chain_has_data(self):
        self.assertEqual(type(self.fut_chain._data), type([]))

    def test_chain_has_count(self):
        self.assertEqual(self.fut_chain.count, self.futures_limit)
        self.assertEqual(len(self.fut_chain), self.futures_limit)

    def test_chain_has_expirations(self):
        data = self.instrument.assetindex.get_futures_list(self.instrument.date, self.instrument,
                                                    self.instrument.futures_limit)
        self.assertEqual(len(self.fut_chain.expirations), self.futures_limit)
        self.assertEqual(self.fut_chain.expirations, [x['expirationdate'] for x in data])

    def test_chain_has_contracts(self):
        self.assertEqual(len(self.fut_chain.contracts), self.futures_limit)
        for f in self.fut_chain.contracts:
            self.assertEqual(type(f), FutureContract)

    def test_chain_has_get_item_byoffset(self):
        self.assertEqual(type(self.fut_chain[0]), FutureContract)
        self.assertEqual(self.fut_chain[0].expiration, datetime(2014, 3, 21, 0, 0))

    def test_chain_get_item_by_expirationdatetime(self):
        self.assertEqual(type(self.fut_chain[datetime(2014, 3, 21, 0, 0)]), FutureContract)
        self.assertEqual(self.fut_chain[datetime(2014, 3, 21, 0, 0)].expiration, datetime(2014, 3, 21, 0, 0))

    def test_chain_get_item_by_expirationdate(self):
        self.assertEqual(type(self.fut_chain[date(2014, 3, 21)]), FutureContract)
        self.assertEqual(self.fut_chain[date(2014, 3, 21)].expiration, datetime(2014, 3, 21, 0, 0))

    def test_chain_has_set_item_byoffset_error(self):
        self.assertRaises(AssertionError, self.fut_chain.__setitem__, 0, None)

    def test_chain_iter_over(self):
        for f in self.fut_chain:
            self.assertEqual(type(f), FutureContract)

    def test_chain_iter_over_items(self):
        for exp, f in self.fut_chain.items():
            self.assertEqual(type(exp), datetime)
            self.assertEqual(type(f), FutureContract)





if __name__ == '__main__':
    unittest.main()
