from exobuilder.contracts.instrument import Instrument
from exobuilder.contracts.futurecontract import FutureContract, FUT_HASH_ROOT
from exobuilder.contracts.optioncontract import OptionContract, OPT_HASH_ROOT

HASH_ROOT_STEP = 100000000

class DataSourceBase(object):
    def __init__(self, assetindex, futures_limit, options_limit, exostorage=None):
        self.assetindex = assetindex
        self.futures_limit = futures_limit
        self.options_limit = options_limit
        self.exostorage = exostorage


    def get_fut_data(self, dbid, date):
        raise NotImplementedError()

    def get_option_data(self, dbid, date):
        raise NotImplementedError()

    def get_extra_data(self, key, date):
        raise NotImplementedError()

    def get(self, item, date):
        if isinstance(item, int):
            #
            # Get item by hash instrument, or future, or option
            #
            if item < FUT_HASH_ROOT:
                raise NotImplementedError("Unknown asset hash")
            elif item < FUT_HASH_ROOT + HASH_ROOT_STEP:
                # Get future contract

                # Fetch contracts meta information from asset index
                fut_contract_dic = self.assetindex.get_future_contract(item - FUT_HASH_ROOT)
                instr_dic = self.assetindex.get_instrument(fut_contract_dic['idinstrument'])

                # Creating contract classes
                instr = Instrument(self, instr_dic, date, self.futures_limit, self.options_limit)
                fut = FutureContract(fut_contract_dic, instr)
                assert fut.__hash__() == item

                return fut
            elif item < OPT_HASH_ROOT + HASH_ROOT_STEP:
                # Get option contract
                # Fetch contracts meta information from asset index
                opt_contract_dic = self.assetindex.get_option_contract(item - OPT_HASH_ROOT)
                fut_contract_dic = self.assetindex.get_future_contract(opt_contract_dic['idcontract'])
                instr_dic = self.assetindex.get_instrument(fut_contract_dic['idinstrument'])

                # Creating contract classes
                instr = Instrument(self, instr_dic, date, self.futures_limit, self.options_limit)
                fut = FutureContract(fut_contract_dic, instr)

                opt = OptionContract(opt_contract_dic, fut)
                assert opt.__hash__() == item

                return opt
            else:
                raise NotImplementedError("Unknown asset hash")
        else:
            #
            # Fetch Instrument by symbol name sting
            #
            data_dict = self.assetindex.get_instrument_info(item)
            return Instrument(self, data_dict, date, self.futures_limit, self.options_limit)
