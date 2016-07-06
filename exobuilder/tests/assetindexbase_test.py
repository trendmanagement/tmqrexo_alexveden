import unittest
from exobuilder.contracts.futureschain import FuturesChain
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.data.assetindex import AssetIndexBase
from .assetindexdict import AssetIndexDicts

from datetime import datetime, date
from exobuilder.contracts.instrument import Instrument


class AssetIndexBaseCase(unittest.TestCase):
    def setUp(self):
        self.assetindex = AssetIndexBase()
        self.symbol = 'EP'
        self.date = datetime(2014, 1, 5, 0, 0, 0)
        self.futures_limit = 12

    def test_notimplemented(self):
        self.assertRaises(NotImplementedError, self.assetindex.get_futures_list, None, None, None)
        self.assertRaises(NotImplementedError, self.assetindex.get_instrument_info, None)
        self.assertRaises(NotImplementedError, self.assetindex.get_options_list, None, None)




if __name__ == '__main__':
    unittest.main()
