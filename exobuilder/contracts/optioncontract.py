from exobuilder.algorithms.blackscholes import blackscholes, blackscholes_greeks
import numpy as np
import warnings

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
    def option_code(self):
        """
        There is a field optioncode in tbloptions that is filled with
        EOM: EW
        WEEKLY: EW1, EW2, EW3, EW4
        WED: E1C, E2C, E3C, E4C, E5C
        The quarterly american options are just filled with ' '
        :return:
        """
        if 'optioncode' not in self._data:
            return ''
        else:
            return self._data['optioncode'].strip()

    @property
    def to_expiration_years(self):
        return (self.expiration.date() - self.date.date()).total_seconds() / 31536000.0 # == (365.0 * 24 * 60 * 60)

    @property
    def to_expiration_days(self):
        return (self.expiration.date() - self.date.date()).days

    def to_expiration_years_from_days(self, days_to_expiration):
        return (days_to_expiration * 24.0 * 60 * 60) / 31536000.0

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

    def price_whatif(self, underlying_price=None, iv_change=0.0, days_to_expiration=None, riskfreerate=None):
        """
        What if analysis pricing depending on various conditions changes
        :param underlying_price: Price option with custom underlying price (if None, use current option price)
        :param iv_change: Price option with custom IV change (in percent points 0.01 - mean that IV rises OptionIV+1%, -0.05 - mean that IV drops OptionIV - 5%)
        :param days_to_expiration: Price option in different days_to_expiration values (0 - mean expired option payoff)
        :param riskfreerate: Set the risk free rate (if None - use the current RFR)
        :return: option price and greeks for set of conditions
        """
        ulprice = self.underlying.price if underlying_price is None else underlying_price
        days_to_expiration = self.to_expiration_days if days_to_expiration is None else days_to_expiration
        riskfreerate = self.riskfreerate if riskfreerate is None else riskfreerate
        iv = self.iv + iv_change

        if days_to_expiration is not None:
            if days_to_expiration > self.to_expiration_days:
                warnings.warn("{0}: WhatIF days to expiration greater than current!".format(self.name), stacklevel=0)


        option_price = blackscholes(self.callorput, ulprice, self.strike, self.to_expiration_years_from_days(days_to_expiration),
                                    riskfreerate, iv)

        options_greeks = blackscholes_greeks(self.callorput, ulprice, self.strike, self.to_expiration_years_from_days(days_to_expiration),
                                             riskfreerate, iv)

        return {
            'asset': self.name,
            'price': option_price,
            'delta': options_greeks[0],
            'ulprice': ulprice,
            'days_to_expiration': days_to_expiration,
            'riskfreerate': riskfreerate,
            'iv': self.iv + iv_change
        }


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

    def __str__(self):
        return '{0} [IV:{1:0.3f} Delta:{2:0.2f}]'.format(self.name, self.iv, self.delta)





