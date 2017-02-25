from collections import OrderedDict
from exobuilder.contracts.optioncontract import OptionContract
from exobuilder.contracts.putcallpair import PutCallPair
from exobuilder.data.exceptions import QuoteNotFoundException
import numpy as np
import bisect
import warnings

class OptionsChain(object):
    def __init__(self, option_chain_dic, futures_contract, options_limit=0):
        self._data = option_chain_dic
        self._fut = futures_contract
        self._options = OrderedDict()
        self._atm_index = -1
        self._options_limit = options_limit

        self._expiration = self._data['_id']['date']

        if options_limit > 0:
            all_strikes = np.array(sorted(list(set([x['strikeprice'] for x in self._data['chain']]))))
            atm_index = np.argmin(np.abs(all_strikes - self.underlying.price))
            all_strikes = all_strikes[max(0, atm_index - options_limit):min(len(self._data['chain']), atm_index + options_limit + 1)]

        self._option_code = None

        for opt_dic in self._data['chain']:
            if options_limit > 0:
                if opt_dic['strikeprice'] not in all_strikes:
                    continue
            option = OptionContract(opt_dic, self._fut)
            pc_pair = self._options.setdefault(option.strike, PutCallPair())
            pc_pair.addoption(option)

            if self._option_code is None:
                self._option_code = option.option_code
            else:
                if self._option_code != option.option_code:
                    raise ValueError("Option chain must contain options with the same option_code values, mixing "
                                     "weeklys with monthly options is not allowed. Check the Asset index DB granularity.")

        self._strike_array = np.array(list(self._options.keys()))

        if len(self._strike_array) == 0:
            raise ValueError("Option chain for {0} is empty".format(futures_contract))

    @property
    def underlying(self):
        return self._fut

    @property
    def instrument(self):
        return self._fut.instrument

    @property
    def expiration(self):
        return self._expiration

    @property
    def to_expiration_days(self):
        return (self.expiration.date() - self._fut.instrument.date.date()).days

    @property
    def contracts(self):
        return self._options

    @property
    def strikes(self):
        return self._strike_array

    @property
    def option_code(self):
        return self._option_code

    def __len__(self):
        return len(self._strike_array)

    def __iter__(self):
        for s, p in self._options.items():
            yield p

    def items(self):
        for s, p in self._options.items():
            yield s, p

    def __setitem__(self, key, value):
        raise AssertionError("Options chain collection is read only")

    def __getitem__(self, item):
        if isinstance(item, (float, np.float64, np.float32)):
            if item not in self._options:
                raise KeyError('Option pair with strike "{0}" not found'.format(item))
            return self._options[item]
        if isinstance(item, (int, np.int32, np.int64)):
            while True:
                if self.atmindex + item < 0 or self.atmindex + item > len(self._strike_array)-1:
                    raise IndexError("Strike offset is too low, [{0}, {1}] values allowed".format(-self.atmindex,
                                                                                                  len(self._strike_array)-self.atmindex-1))
                strike = self._strike_array[self.atmindex + item]
                pc_pair = self._options[strike]
                try:
                    # Getting Put/Call prices
                    # To make sure that we have quotes available in the DB
                    pc_pair.C.price
                    pc_pair.P.price
                    return pc_pair
                except QuoteNotFoundException:
                    # Searching next strike
                    if item >= 0:
                        item += 1
                    else:
                        item -= 1
        else:
            raise ValueError('Unexpected item type, must be float or int')

    def get_by_delta(self, delta):
        """
        Search option contract by delta value:
        If delta ==  0.5 - returns ATM call
        If delta == -0.5 - returns ATM put

        If delta > 0.5 - returns ITM call near target delta
        If delta < -0.5 - returns ITM put near target delta

        If delta > 0 and < 0.5 - returns OTM call
        If delta < 0 and > -0.5 - returns OTM put

        If delta <= -1 or >= 1 or 0 - raises error
        :param delta: value of delta contract to find
        :return: Option contract instance
        """
        if delta <= -1 or delta >= 1 or delta == 0 or np.isnan(delta):
            raise ValueError("Delta values must be > -1 and < 1")

        if delta == 0.5:
            return self[0].C
        if delta == -0.5:
            return self[0].P

        if delta < -0.5:
            i = 1
            # Search for ITM put
            while i <= self.maxoffset:
                try:
                    if self[i].P.delta <= delta:
                        return self[i].P
                except QuoteNotFoundException:
                    # Catching data errors is the contract has custom strike
                    pass
                i += 1

            # Can't find suitable delta
            last_option = self[self.maxoffset].P
            warnings.warn("Can't find contract with delta: {0} using last available contract in chain: {1}".format(delta, last_option))
            return last_option


        if delta < 0 and delta > -0.5:
            # Search for OTM put
            i = -1
            while i >= self.minoffset:
                try:
                    if self[i].P.delta >= delta:
                        return self[i].P
                except QuoteNotFoundException:
                    # Catching data errors is the contract has custom strike
                    pass
                i -= 1

            # Can't find suitable delta
            last_option = self[self.minoffset].P
            warnings.warn(
                "Can't find contract with delta: {0} using last available contract in chain: {1}".format(delta,
                                                                                                         last_option))
            return last_option


        if delta > 0.5:
            # Search for ITM call
            i = -1
            while i >= self.minoffset:
                try:
                    if self[i].C.delta >= delta:
                        return self[i].C
                except QuoteNotFoundException:
                    # Catching data errors is the contract has custom strike
                    pass

                i -= 1

            # Can't find suitable delta
            last_option = self[self.minoffset].C
            warnings.warn(
                "Can't find contract with delta: {0} using last available contract in chain: {1}".format(delta,
                                                                                                         last_option))
            return last_option

        if delta > 0 and delta < 0.5:
            i = 1
            # Search for OTM call
            while i <= self.maxoffset:
                try:
                    if self[i].C.delta <= delta:
                        return self[i].C
                except QuoteNotFoundException:
                    # Catching data errors is the contract has custom strike
                    pass
                i += 1

            # Can't find suitable delta
            last_option = self[self.maxoffset].C
            warnings.warn(
                "Can't find contract with delta: {0} using last available contract in chain: {1}".format(delta,
                                                                                                         last_option))
            return last_option

        raise NotImplementedError("Unexpected code flow")

    @property
    def maxoffset(self):
        return len(self._strike_array) - self.atmindex - 1

    @property
    def minoffset(self):
        return -self.atmindex


    @property
    def atmstrike(self):
        return self._strike_array[self.atmindex]

    @property
    def atmindex(self):
        if self._atm_index == -1:
            ulprice = self.underlying.price
            self._atm_index = np.argmin(np.abs(self._strike_array - ulprice))
        return self._atm_index

    def __repr__(self):
        opt_str = ""

        atmi = self.atmindex

        for i, strike in enumerate(self.strikes):
            opt_str += "{0}: {1}\n".format(i-atmi, self[strike])
        return opt_str