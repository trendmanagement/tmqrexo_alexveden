import unittest
from exobuilder.contracts.futureschain import FuturesChain
from exobuilder.contracts.futurecontract import FutureContract
from exobuilder.contracts.optioncontract import OptionContract
from .assetindexdict import AssetIndexDicts
from datetime import datetime, date
from exobuilder.contracts.instrument import Instrument

class OptionContractTestCase(unittest.TestCase):
    def setUp(self):
        self.instrument = Instrument
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

        self.opt_contract_dict = {'_id': '577a573e4b01f47f84d0cbd5',
                                'callorput': 'p',
                                'cqgsymbol': 'P.US.EPH1427750',
                                'expirationdate': datetime(2014, 3, 21, 0, 0),
                                'idcontract': 4736,
                                'idinstrument': 11,
                                'idoption': 11558454,
                                'optionmonth': 'H',
                                'optionmonthint': 3,
                                'optionname': 'P.US.EPH1427750',
                                'optionyear': 2014,
                                'strikeprice': 2775.0
                              }

        self.option_contract = OptionContract(self.opt_contract_dict, self.fut_contract)

    def test_constructor(self):
        opt_contract = OptionContract(self.opt_contract_dict, self.fut_contract)
        self.assertEqual(type(opt_contract._data), dict)
        self.assertEqual(type(opt_contract._future_contract), FutureContract)

    def test_optioncontract_has_name(self):
        self.assertEqual(self.option_contract.name, self.opt_contract_dict['optionname'])

    def test_optioncontract_has_underlying(self):
        self.assertEqual(self.option_contract.underlying, self.fut_contract)

    def test_optioncontract_has_strike(self):
        self.assertEqual(self.option_contract.strike, self.opt_contract_dict['strikeprice'])

    def test_optioncontract_has_instrument(self):
        self.assertEqual(self.option_contract.instrument, self.instrument)

    def test_optioncontract_has_expiration(self):
        self.assertEqual(self.option_contract.expiration, self.opt_contract_dict['expirationdate'])

    def test_optioncontract_has_callorput_uppercase(self):
        self.assertEqual(self.option_contract.callorput, 'P')

    def test_optioncontract_has_putorcall_uppercase(self):
        self.assertEqual(self.option_contract.putorcall, 'P')

    def test_optioncontract_has_dbid(self):
        self.assertEqual(self.option_contract.dbid, self.opt_contract_dict['idoption'])




if __name__ == '__main__':
    unittest.main()
