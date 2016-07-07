from exobuilder.contracts.optionexpirationchain import OptionExpirationChain

class FutureContract(object):
    def __init__(self, contract_dic, instrument):
        """
        Futures contract class
        :param contract_dic: asset index futures contract dict
        :param instrument: underlying instrument class
        """
        self._data = contract_dic
        self._instrument = instrument
        self._price = 0.0
        self._options = None

    @property
    def name(self):
        return self._data['contractname']

    @property
    def expiration(self):
        return self._data['expirationdate']

    @property
    def instrument(self):
        return self._instrument

    @property
    def dbid(self):
        return self._data['idcontract']

    @property
    def price(self):
        return self._price

    @property
    def options(self):
        if self._options is None:
            opt_chain_dict = self._instrument.assetindex.get_options_list(self._instrument.date, self)
            self._options = OptionExpirationChain(opt_chain_dict, self)
        return self._options


