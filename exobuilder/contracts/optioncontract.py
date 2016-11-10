from exobuilder.algorithms.blackscholes import blackscholes, blackscholes_greeks
import numpy as np

OPT_HASH_ROOT = 200000000

class OptionContract(object):
    contract_type = 'opt'

    def __init__(self, contract_dic, future_contract):
        """
        Option contract class
        :param contract_dic: option contract definition from DB
        :param future_contract: futures contract class instance
        """
        self._data = contract_dic
        self._future_contract = future_contract
        self._option_price_data = None
        self._option_price = float('nan')
        self._options_greeks = None

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

    @property
    def month_int(self):
        return self._data['optionmonthint']

    @property
    def date(self):
        return self.instrument.date

    @property
    def to_expiration_years(self):
        return (self.expiration.date() - self.date.date()).total_seconds() / 31536000.0 # == (365.0 * 24 * 60 * 60)

    @property
    def to_expiration_days(self):
        return (self.expiration.date() - self.date.date()).days

    @property
    def riskfreerate(self):
        return self.instrument.datasource.get_extra_data('riskfreerate', self.date)

    @property
    def iv(self):
        if self._option_price_data is None:
            self._option_price_data = self.instrument.datasource.get_option_data(self.dbid, self.date)
        return self._option_price_data["impliedvol"]

    @property
    def price(self):
        if np.isnan(self._option_price):
            self._option_price = blackscholes(self.callorput, self.underlying.price, self.strike, self.to_expiration_years, self.riskfreerate, self.iv)

        return self._option_price

    @property
    def delta(self):
        if self._options_greeks is None:
            self._options_greeks = blackscholes_greeks(self.callorput, self.underlying.price, self.strike, self.to_expiration_years, self.riskfreerate, self.iv)

        return self._options_greeks[0]

    @property
    def pointvalue(self):
        return self.instrument.point_value_options

    def as_dict(self):
        return {'name': self.name, 'dbid': self.dbid, 'type': 'O', 'hash': self.__hash__()}

    def __hash__(self):
        return OPT_HASH_ROOT + self.dbid

    def __eq__(self, other):
        if isinstance(other, OptionContract) and other.__hash__() == self.__hash__():
            return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)





