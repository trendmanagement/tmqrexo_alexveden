from exobuilder.contracts.optionexpirationchain import OptionExpirationChain

FUT_HASH_ROOT = 100000000

class FutureContract(object):
    def __init__(self, contract_dic, instrument):
        """
        Futures contract class
        :param contract_dic: asset index futures contract dict
        :param instrument: underlying instrument class
        """
        self._data = contract_dic
        self._instrument = instrument
        self._options = None
        self._price_data = None
        self._price = 0.0

    @property
    def name(self):
        return self._data['contractname']

    @property
    def expiration(self):
        return self._data['expirationdate']

    @property
    def to_expiration_days(self):
        return (self.expiration.date() - self.date.date()).days

    @property
    def date(self):
        return self._instrument.date

    @property
    def instrument(self):
        return self._instrument

    @property
    def month_int(self):
        return self._data['monthint']

    @property
    def dbid(self):
        return self._data['idcontract']

    @property
    def price(self):
        if self._price == 0.0:
            # Getting price data from datasource
            self._price_data = self._instrument.datasource.get_fut_data(self.dbid, self._instrument.date)
            self._price = self._price_data['close']

        return self._price

    @property
    def price_quote_date(self):
        if self._price_data is None:
            # Implicitly set _price_date by calling self.price
            x = self.price
        return self._price_data['bartime']

    @property
    def delta(self):
        # For future contract delta is always = 1.0
        return 1.0

    @property
    def pointvalue(self):
        return self.instrument.point_value_futures

    @property
    def options(self):
        if self._options is None:
            opt_chain_dict = self._instrument.assetindex.get_options_list(self._instrument.date, self)
            self._options = OptionExpirationChain(opt_chain_dict, self)
        return self._options

    def __str__(self):
        return '{0} {1} {2}'.format(self.expiration.date(), self.name, self.price)

    def __repr__(self):
        return '{0} {1} {2}'.format(self.expiration.date(), self.name, self.price)

    def as_dict(self):
        return {'name': self.name, 'dbid': self.dbid, 'type': 'F', 'hash': self.__hash__()}

    def __hash__(self):
        return FUT_HASH_ROOT + self.dbid

    def __eq__(self, other):
        if isinstance(other, FutureContract) and other.__hash__() == self.__hash__():
            return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)


