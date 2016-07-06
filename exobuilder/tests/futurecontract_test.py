import unittest
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.contracts.instrument import Instrument
import datetime

class FutureContractTestCase(unittest.TestCase):
    def setUp(self):
        self.instrument = Instrument
        self.contract_dict = {'_id': '577a4fa34b01f47f84cab23c',
                              'contractname': 'F.EPZ16',
                              'cqgsymbol': 'F.EPZ16',
                              'expirationdate': datetime.datetime(2016, 12, 16, 0, 0),
                              'idcontract': 6570,
                              'idinstrument': 11,
                              'month': 'Z',
                              'monthint': 12,
                              'year': 2016}
        self.fut_contract = FutureContract(self.contract_dict, self.instrument)

    def test_constructor(self):
        fut = FutureContract(self.contract_dict, self.instrument)
        self.assertEqual(fut._data, self.contract_dict)

    def test_future_has_name(self):
        self.assertEqual(self.fut_contract.name, self.contract_dict['contractname'])

    def test_future_has_expiration(self):
        self.assertEqual(self.fut_contract.expiration, self.contract_dict['expirationdate'])

    def test_future_has_instrument(self):
        self.assertEqual(self.fut_contract.instrument, self.instrument)

    def test_future_has_dbid(self):
        self.assertEqual(self.fut_contract.dbid, self.contract_dict['idcontract'])


if __name__ == '__main__':
    unittest.main()
