

class FutureContract(object):
    def __init__(self, contract_dic, instrument):
        """
        Futures contract class
        :param contract_dic: asset index futures contract dict
        :param instrument: underlying instrument class
        """
        self._data = contract_dic
        self._instrument = instrument

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

