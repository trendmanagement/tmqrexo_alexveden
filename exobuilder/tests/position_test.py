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


    def test_add(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3)
        pos.add(trans)

        positions = pos.netpositions
        self.assertEqual(1, len(positions))
        self.assertEqual(True, self.fut_contract in positions)
        p = positions[self.fut_contract]

        self.assertEqual(p['qty'], 4.0)
        self.assertEqual(p['value'], trans.usdvalue)
        self.assertEqual(0, pos._realized_pnl)

    def test_add_2transactions(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3)
        pos.add(trans)

        trans2 = Transaction(self.fut_contract, self.date, 2.0, 15.3)
        pos.add(trans2)

        positions = pos.netpositions
        self.assertEqual(1, len(positions))
        self.assertEqual(True, self.fut_contract in positions)
        p = positions[self.fut_contract]

        self.assertEqual(p['qty'], 6.0)
        self.assertEqual(p['value'], trans.usdvalue + trans2.usdvalue)
        self.assertEqual(0, pos._realized_pnl)

    def test_add_to_closeposition_long(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3)
        pos.add(trans)

        trans = Transaction(self.fut_contract, self.date, -4.0, 13.3)
        pos.add(trans)

        positions = pos.netpositions
        self.assertEqual(0, len(positions))
        self.assertEqual(200, pos._realized_pnl)

    def test_add_to_closeposition_short(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, -4.0, 12.3)
        pos.add(trans)

        trans = Transaction(self.fut_contract, self.date, 4.0, 13.3)
        pos.add(trans)

        positions = pos.netpositions
        self.assertEqual(0, len(positions))
        self.assertEqual(-200, pos._realized_pnl)

    def test_add_shrink_position_short(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, -4.0, 12.3)
        pos.add(trans)

        trans2 = Transaction(self.fut_contract, self.date, 2.0, 13.3)
        pos.add(trans2)

        positions = pos.netpositions
        self.assertEqual(1, len(positions))
        self.assertEqual(-100, pos._realized_pnl)

        self.assertEqual(1, len(positions))
        self.assertEqual(True, self.fut_contract in positions)
        p = positions[self.fut_contract]

        self.assertEqual(p['qty'], -2.0)
        self.assertEqual(p['value'], trans.usdvalue / 2)

    def test_add_shrink_position_long(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3)
        pos.add(trans)

        trans2 = Transaction(self.fut_contract, self.date, -2.0, 13.3)
        pos.add(trans2)

        positions = pos.netpositions
        self.assertEqual(1, len(positions))
        self.assertEqual(100, pos._realized_pnl)

        self.assertEqual(1, len(positions))
        self.assertEqual(True, self.fut_contract in positions)
        p = positions[self.fut_contract]

        self.assertEqual(p['qty'], 2.0)
        self.assertEqual(p['value'], trans.usdvalue / 2)

    def test_add_shrink_position_short_and_then_close(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, -4.0, 12.3)
        pos.add(trans)

        trans2 = Transaction(self.fut_contract, self.date, 2.0, 13.3)
        pos.add(trans2)

        trans3 = Transaction(self.fut_contract, self.date, 2.0, 13.3)
        pos.add(trans3)

        positions = pos.netpositions
        self.assertEqual(0, len(positions))
        self.assertEqual(-200, pos._realized_pnl)

    def test_add_shrink_position_long_and_then_close(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3)
        pos.add(trans)

        trans2 = Transaction(self.fut_contract, self.date, -2.0, 13.3)
        pos.add(trans2)

        trans3 = Transaction(self.fut_contract, self.date, -2.0, 13.3)
        pos.add(trans3)

        positions = pos.netpositions
        self.assertEqual(0, len(positions))
        self.assertEqual(200, pos._realized_pnl)

    def test_add_shrink_position_long_pnl(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3)
        pos.add(trans)

        trans2 = Transaction(self.fut_contract, self.date, -2.0, 13.3)
        pos.add(trans2)

        positions = pos.netpositions
        self.assertEqual(1, len(positions))
        self.assertEqual(100, pos._realized_pnl)

        self.assertEqual(1, len(positions))
        self.assertEqual(True, self.fut_contract in positions)
        p = positions[self.fut_contract]

        self.assertEqual(p['qty'], 2.0)
        self.assertEqual(p['value'], trans.usdvalue / 2)

        self.fut_contract._price = 14.3
        self.assertEqual(pos.pnl, 100+200)

    def test_add_shrink_position_short_pnl(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, -4.0, 12.3)
        pos.add(trans)

        trans2 = Transaction(self.fut_contract, self.date, 2.0, 13.3)
        pos.add(trans2)

        positions = pos.netpositions
        self.assertEqual(1, len(positions))
        self.assertEqual(-100, pos._realized_pnl)

        self.assertEqual(1, len(positions))
        self.assertEqual(True, self.fut_contract in positions)
        p = positions[self.fut_contract]

        self.assertEqual(p['qty'], -2.0)
        self.assertEqual(p['value'], trans.usdvalue / 2)

        self.fut_contract._price = 14.3
        self.assertEqual(pos.pnl, -100-200)

    def test_add_to_closeposition_long_pnl(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3)
        pos.add(trans)

        trans = Transaction(self.fut_contract, self.date, -4.0, 13.3)
        pos.add(trans)

        positions = pos.netpositions
        self.assertEqual(0, len(positions))
        self.assertEqual(200, pos._realized_pnl)
        self.assertEqual(200, pos.pnl)

    def test_add_to_closeposition_short_pnl(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, -4.0, 12.3)
        pos.add(trans)

        trans = Transaction(self.fut_contract, self.date, 4.0, 13.3)
        pos.add(trans)

        positions = pos.netpositions
        self.assertEqual(0, len(positions))
        self.assertEqual(-200, pos._realized_pnl)
        self.assertEqual(-200, pos.pnl)

    def test_as_dict(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3, leg_name='leg1')
        pos.add(trans)

        trans2 = Transaction(self.fut_contract, self.date, -2.0, 13.3)
        pos.add(trans2)

        positions = pos.netpositions
        self.assertEqual(1, len(positions))
        self.assertEqual(100, pos._realized_pnl)

        self.assertEqual(1, len(positions))
        self.assertEqual(True, self.fut_contract in positions)
        p = positions[self.fut_contract]

        self.assertEqual(p['qty'], 2.0)
        self.assertEqual(p['value'], trans.usdvalue / 2)

        self.fut_contract._price = 14.3
        self.assertEqual(100, pos._realized_pnl)
        self.assertEqual(pos.pnl, 100 + 200)

        self.assertEqual({'positions':
                              {
                                  str(self.fut_contract.__hash__()): {'qty': 2.0, 'value': trans.usdvalue/2, 'leg_name': 'leg1'}
                              },
            '_realized_pnl': 100.0
        }, pos.as_dict())


    def test_from_dict(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3, leg_name='fut1')
        pos.add(trans)

        trans2 = Transaction(self.fut_contract, self.date, -2.0, 13.3)
        pos.add(trans2)

        positions = pos.netpositions
        self.assertEqual(1, len(positions))
        self.assertEqual(100, pos._realized_pnl)

        self.assertEqual(1, len(positions))
        self.assertEqual(True, self.fut_contract in positions)
        p = positions[self.fut_contract]

        self.assertEqual(p['qty'], 2.0)
        self.assertEqual(p['value'], trans.usdvalue / 2)

        self.fut_contract._price = 14.3
        self.assertEqual(100, pos._realized_pnl)
        self.assertEqual(pos.pnl, 100 + 200)

        pos_dic = pos.as_dict()

        # Deserealizing position

        p2 = Position.from_dict(pos_dic, self.datasource, self.date)

        positions = p2.netpositions
        self.assertEqual(100, p2._realized_pnl)

        self.assertEqual(1, len(positions))
        self.assertEqual(True, self.fut_contract in positions)
        p = positions[self.fut_contract]

        # Wrong - because we have new object from datsource
        #self.fut_contract._price = 14.3

        for k in positions.keys():
            k._price = 14.3

        self.assertEqual(p['qty'], 2.0)
        self.assertEqual(p['value'], trans.usdvalue / 2)

        self.assertEqual(1, len(p2.legs))
        self.assertEqual(True, 'fut1' in p2.legs)
        self.assertEqual(self.fut_contract, p2.legs['fut1'])

        self.assertEqual(100, p2._realized_pnl)
        self.assertEqual(p2.pnl, 100 + 200)

    def test_has_len(self):
        pos = Position()
        self.assertEqual(len(pos), 0)
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3)
        pos.add(trans)
        self.assertEqual(len(pos), 1)

    def test_close_all(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3, leg_name='fut1')
        pos.add(trans)

        trans2 = Transaction(self.fut_contract, self.date, 2.0, 15.3)
        pos.add(trans2)

        positions = pos.netpositions
        self.assertEqual(1, len(positions))
        self.assertEqual(True, self.fut_contract in positions)
        p = positions[self.fut_contract]

        self.assertEqual(p['qty'], 6.0)
        self.assertEqual(p['value'], trans.usdvalue + trans2.usdvalue)
        self.assertEqual(0, pos._realized_pnl)

        self.fut_contract._price = 14.3
        trans = pos.close_all_translist()
        self.assertEqual([Transaction(self.fut_contract, self.date, -6.0, 14.3)], trans)
        self.assertEqual('fut1', trans[0].leg_name)
        self.assertNotEqual(None, Transaction(self.fut_contract, self.date, -6.0, 14.3)) # For 100% coverage

    def test_add_leg_has_legs(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3, leg_name='fut1')
        pos.add(trans)

        self.assertEqual(True, 'fut1' in pos.legs)

    def test_add_leg_has_no_legs_if_leg_name_is_empty(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3, leg_name='')
        pos.add(trans)

        self.assertEqual(False, 'fut1' in pos.legs)

    def test_add_leg_delete_leg_is_position_closed(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3, leg_name='fut1')
        pos.add(trans)

        self.assertEqual(True, 'fut1' in pos.legs)
        self.assertEqual(1, len(pos.legs))

        trans = Transaction(self.fut_contract, self.date, -4.0, 12.3, leg_name='')
        pos.add(trans)

        self.assertEqual(False, 'fut1' in pos.legs)
        self.assertEqual(0, len(pos.legs))

    def test_add_leg_expection_if_leg_name_duplicate_but_different_assets(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3, leg_name='fut1')
        pos.add(trans)

        self.assertEqual(True, 'fut1' in pos.legs)
        self.assertEqual(1, len(pos.legs))

        contract_dict = {'_id': '577a4fa34b01f47f84cab23c',
                              'contractname': 'F.EPZ16',
                              'cqgsymbol': 'F.EPZ16',
                              'expirationdate': datetime(2016, 12, 16, 0, 0),
                              'idcontract': 650,
                              'idinstrument': 11,
                              'month': 'Z',
                              'monthint': 12,
                              'year': 2016}
        fut_contract2 = FutureContract(contract_dict, self.instrument)

        trans = Transaction(fut_contract2, self.date, -4.0, 12.3, leg_name='fut1')
        self.assertRaises(NameError, pos.add, trans)

    def test_add_2_different_legs(self):
        pos = Position()
        trans = Transaction(self.fut_contract, self.date, 4.0, 12.3, leg_name='fut1')
        pos.add(trans)

        self.assertEqual(True, 'fut1' in pos.legs)
        self.assertEqual(1, len(pos.legs))

        contract_dict = {'_id': '577a4fa34b01f47f84cab23c',
                              'contractname': 'F.EPZ16',
                              'cqgsymbol': 'F.EPZ16',
                              'expirationdate': datetime(2016, 12, 16, 0, 0),
                              'idcontract': 650,
                              'idinstrument': 11,
                              'month': 'Z',
                              'monthint': 12,
                              'year': 2016}
        fut_contract2 = FutureContract(contract_dict, self.instrument)

        trans = Transaction(fut_contract2, self.date, -4.0, 12.3, leg_name='fut2')
        pos.add(trans)

        self.assertEqual(2, len(pos.legs))
        self.assertEqual(True, 'fut1' in pos.legs)
        self.assertEqual(True, 'fut2' in pos.legs)
        self.assertEqual(fut_contract2, pos.legs['fut2'])
        self.assertEqual(self.fut_contract, pos.legs['fut1'])





