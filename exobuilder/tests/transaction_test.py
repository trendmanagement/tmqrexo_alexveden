import unittest
from datetime import datetime

from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.exo.transaction import Transaction
from .assetindexdict import AssetIndexDicts
from .datasourcefortest import DataSourceForTest


class TransactionTestCase(unittest.TestCase):
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

    def test_constructor(self):
        t = Transaction(self.fut_contract, self.date, 4.0, 12.3)

        self.assertEqual(t._asset, self.fut_contract)
        self.assertEqual(t._date, self.date)
        self.assertEqual(t._qty, 4.0)
        self.assertEqual(t._price, 12.3)

    def test_has_asset(self):
        self.assertEqual(self.trans.asset, self.fut_contract)

    def test_has_date(self):
        self.assertEqual(self.trans.date, self.date)

    def test_has_qty(self):
        self.assertEqual(self.trans.qty, 4.0)

    def test_has_price(self):
        self.assertEqual(self.trans.price, 12.3)

    def test_has_usdvalue(self):
        self.assertEqual(self.trans.usdvalue, 4*12.3*self.fut_contract.pointvalue)

    def test_has_as_dict(self):
        self.assertEqual({'date': self.trans.date,
                          'qty': self.trans.qty,
                          'price': self.trans.price,
                          'asset': self.fut_contract.as_dict(),
                          'usdvalue': self.trans.usdvalue}, self.trans.as_dict())

