from collections import OrderedDict
from exobuilder.contracts.optioncontract import OptionContract
from exobuilder.contracts.putcallpair import PutCallPair
import numpy as np
import bisect


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

        for opt_dic in self._data['chain']:
            if options_limit > 0:
                if opt_dic['strikeprice'] not in all_strikes:
                    continue
            option = OptionContract(opt_dic, self._fut)
            pc_pair = self._options.setdefault(option.strike, PutCallPair())
            pc_pair.addoption(option)
        self._strike_array = np.array(list(self._options.keys()))

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
    def contracts(self):
        return self._options

    @property
    def strikes(self):
        return self._strike_array

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
            if self.atmindex + item < 0 or self.atmindex + item > len(self._strike_array)-1:
                raise IndexError("Strike offset is too low, [{0}, {1}] values allowed".format(-self.atmindex, len(self._strike_array)-self.atmindex-1))
            strike = self._strike_array[self.atmindex + item]
            return self._options[strike]
        else:
            raise ValueError('Unexpected item type, must be float or int')

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