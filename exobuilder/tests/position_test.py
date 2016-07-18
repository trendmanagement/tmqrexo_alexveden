import unittest
from datetime import datetime

from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.exo.transaction import Transaction
from exobuilder.exo.position import Position
from .assetindexdict import AssetIndexDicts
from .datasourcefortest import DataSourceForTest

class PositionTestCase(unittest.TestCase):
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


    def test_add(self):
        pos = Position()
        pos.add(self.fut_contract, self.date, 4.0, 12.3)

        trans = pos.transactions
        self.assertEqual(1, len(trans))
        t = trans[0]
        self.assertEqual(t.asset, self.fut_contract)
        self.assertEqual(t.date, self.date)
        self.assertEqual(t.qty, 4.0)
        self.assertEqual(t.price, 12.3)

    def test_net_positions_opened(self):
        pos = Position()
        pos.add(self.fut_contract, self.date, 4.0, 12.3)

        trans = pos.transactions
        self.assertEqual(1, len(trans))

        netpositions = pos.netpositions
        self.assertTrue(trans[0].asset in netpositions)

        p = netpositions[trans[0].asset]
        self.assertEqual(p['qty'], 4.0)
        self.assertEqual(p['value'], -trans[0].usdvalue)

    def test_net_positions_opened_and_closed(self):
        pos = Position()
        pos.add(self.fut_contract, self.date, 4.0, 12.3)

        trans = pos.transactions
        self.assertEqual(1, len(trans))

        netpositions = pos.netpositions
        self.assertTrue(trans[0].asset in netpositions)
        self.assertEqual(1, len(netpositions))

        p = netpositions[trans[0].asset]
        self.assertEqual(p['qty'], 4.0)
        self.assertEqual(p['value'], -trans[0].usdvalue)

        # Closing opened position
        pos.add(self.fut_contract, self.date, -4.0, 12.3)
        trans = pos.transactions
        self.assertEqual(2, len(trans))

        netpositions = pos.netpositions
        self.assertTrue(trans[0].asset in netpositions)
        self.assertTrue(trans[1].asset in netpositions)
        self.assertEqual(1, len(netpositions))

        p = netpositions[trans[0].asset]
        self.assertEqual(p['qty'], 0.0)
        self.assertEqual(p['value'], 0)

    def test_net_positions_opened_and_closed_profit(self):
        pos = Position()
        pos.add(self.fut_contract, self.date, 4.0, 12.3)

        trans = pos.transactions
        self.assertEqual(1, len(trans))

        netpositions = pos.netpositions
        self.assertTrue(trans[0].asset in netpositions)
        self.assertEqual(1, len(netpositions))

        p = netpositions[trans[0].asset]
        self.assertEqual(p['qty'], 4.0)
        self.assertEqual(p['value'], -trans[0].usdvalue)

        # Closing opened position
        pos.add(self.fut_contract, self.date, -4.0, 13.3)
        trans = pos.transactions
        self.assertEqual(2, len(trans))

        netpositions = pos.netpositions
        self.assertTrue(trans[0].asset in netpositions)
        self.assertTrue(trans[1].asset in netpositions)
        self.assertEqual(1, len(netpositions))

        p = netpositions[trans[0].asset]
        self.assertEqual(p['qty'], 0.0)
        self.assertEqual(p['value'], 50*4)

    def test_net_positions_opened_and_3_transactions(self):
        pos = Position()
        pos.add(self.fut_contract, self.date, 4.0, 12.3)

        trans = pos.transactions
        self.assertEqual(1, len(trans))

        netpositions = pos.netpositions
        self.assertTrue(trans[0].asset in netpositions)
        self.assertEqual(1, len(netpositions))

        p = netpositions[trans[0].asset]
        self.assertEqual(p['qty'], 4.0)
        self.assertEqual(p['value'], -trans[0].usdvalue)

        # Closing opened position
        pos.add(self.fut_contract, self.date, -5.0, 13.3)
        pos.add(self.fut_contract, self.date, 1.0, 13.3)
        trans = pos.transactions
        self.assertEqual(3, len(trans))

        netpositions = pos.netpositions
        self.assertTrue(trans[0].asset in netpositions)
        self.assertTrue(trans[1].asset in netpositions)
        self.assertTrue(trans[2].asset in netpositions)
        self.assertEqual(1, len(netpositions))

        p = netpositions[trans[0].asset]
        self.assertEqual(p['qty'], 0.0)
        self.assertEqual(p['value'], 50 * 4)

    def test_pnl_opened_position(self):
        pos = Position()

        pos.add(self.fut_contract, self.date, 4.0, 12.3)

        trans = pos.transactions
        self.assertEqual(1, len(trans))

        self.fut_contract._price = 13.3

        self.assertEqual(pos.pnl, 200)

    def test_pnl_closed_profit(self):
        pos = Position()

        pos.add(self.fut_contract, self.date, 4.0, 12.3)
        pos.add(self.fut_contract, self.date, -4.0, 14.3)
        trans = pos.transactions
        self.assertEqual(2, len(trans))

        self.fut_contract._price = 13.3

        self.assertEqual(pos.pnl, 400)

    def test_pnl_open_profit_average_price(self):
        pos = Position()

        pos.add(self.fut_contract, self.date, 4.0, 12.3)
        pos.add(self.fut_contract, self.date, 4.0, 14.3)
        trans = pos.transactions
        self.assertEqual(2, len(trans))

        self.fut_contract._price = 15.3

        self.assertEqual(pos.pnl, 3*200+1*200)

    def test_close(self):
        self.fut_contract._price = 15.3

        pos = Position()
        pos.add(self.fut_contract, self.date, 4.0, 12.3)
        trans = pos.transactions
        pos.close(self.date)
        self.assertEqual(2, len(trans))

        t = trans[1]


        self.assertEqual(t.asset.price, 15.3)
        self.assertEqual(t.asset, self.fut_contract)
        self.assertEqual(t.date, self.date)
        self.assertEqual(t.qty, -4.0)
        self.assertEqual(t.price, 15.3)
        self.assertEqual(pos.pnl, 3*200)

    def test_has_isclosed(self):
        self.fut_contract._price = 15.3

        pos = Position()
        pos.add(self.fut_contract, self.date, 4.0, 12.3)
        self.assertEqual(False, pos.is_closed)
        pos.close(self.date)
        self.assertEqual(True, pos.is_closed)

    def test_add_transaction(self):
        pos = Position()
        _t = Transaction(self.fut_contract, self.date, 4.0, 12.3)
        pos.add_transaction(_t)

        trans = pos.transactions
        self.assertEqual(1, len(trans))
        t = trans[0]
        self.assertEqual(t, _t)
        self.assertEqual(t.asset, self.fut_contract)
        self.assertEqual(t.date, self.date)
        self.assertEqual(t.qty, 4.0)
        self.assertEqual(t.price, 12.3)






if __name__ == '__main__':
    unittest.main()
