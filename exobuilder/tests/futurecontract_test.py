import unittest
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.contracts.instrument import Instrument
from exobuilder.contracts.optionexpirationchain import OptionExpirationChain
from .datasourcefortest import DataSourceForTest
from .assetindexdict import AssetIndexDicts
from datetime import datetime

class FutureContractTestCase(unittest.TestCase):
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

    def test_constructor(self):
        fut = FutureContract(self.contract_dict, self.instrument)
        self.assertEqual(fut._data, self.contract_dict)
        self.assertEqual(fut._price, 0.0)

    def test_future_has_name(self):
        self.assertEqual(self.fut_contract.name, self.contract_dict['contractname'])

    def test_future_has_expiration(self):
        self.assertEqual(self.fut_contract.expiration, self.contract_dict['expirationdate'])

    def test_future_has_instrument(self):
        self.assertEqual(self.fut_contract.instrument, self.instrument)

    def test_future_has_dbid(self):
        self.assertEqual(self.fut_contract.dbid, self.contract_dict['idcontract'])

    def test_future_has_price(self):
        self.fut_contract._price = 1500
        self.assertEqual(self.fut_contract.price, 1500)

    def test_future_has_expirations(self):
        self.assertEqual(type(self.fut_contract.options), OptionExpirationChain)

    def test_future_has_expirations_and_cached(self):
        fut = FutureContract(self.contract_dict, self.instrument)
        options = id(fut.options)
        self.assertEqual(id(fut.options), options)

    def test_future_str_format(self):
        fut = FutureContract(self.contract_dict, self.instrument)
        self.assertEqual(str(fut), '{0} {1} {2}'.format(fut.expiration.date(), fut.name, fut.price))

    def test_future_repr_format(self):
        fut = FutureContract(self.contract_dict, self.instrument)
        self.assertEqual(fut.__repr__(), '{0} {1} {2}'.format(fut.expiration.date(), fut.name, fut.price))

    def test_has_point_value(self):
        point_val = self.fut_contract.pointvalue
        self.assertEqual(self.fut_contract.instrument.point_value_futures, point_val)


if __name__ == '__main__':
    unittest.main()
