

class OptionContract(object):
    def __init__(self, contract_dic, future_contract):
        """
        Option contract class
        :param contract_dic: option contract definition from DB
        :param future_contract: futures contract class instance
        """
        self._data = contract_dic
        self._future_contract = future_contract

    @property
    def name(self):
        return self._data['optionname']

    @property
    def underlying(self):
        return self._future_contract

    @property
    def strike(self):
        return self._data['strikeprice']

    @property
    def instrument(self):
        return self._future_contract.instrument

    @property
    def expiration(self):
        return self._data['expirationdate']

    @property
    def callorput(self):
        return self._data['callorput'].upper()

    @property
    def putorcall(self):
        return self._data['callorput'].upper()

    @property
    def dbid(self):
        return self._data['idoption']
