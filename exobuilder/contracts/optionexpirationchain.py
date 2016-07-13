from collections import OrderedDict
from exobuilder.contracts.optionschain import OptionsChain
from datetime import datetime, date
import numpy as np


class OptionExpirationChain(object):
    def __init__(self, expiration_chain_dict, future_contract):
        self._data = expiration_chain_dict
        self._fut = future_contract
        self._chains = OrderedDict()

        for record in self._data:
            option_chain = OptionsChain(record, self._fut, self._fut.instrument.options_limit)
            self._chains[option_chain.expiration] = option_chain

        self._expirations = sorted(list(self._chains.keys()))

    @property
    def expirations(self):
        return self._expirations

    def __len__(self):
        return len(self._chains)

    def __iter__(self):
        for k, v in self._chains.items():
            yield v

    def items(self):
        for k, v in self._chains.items():
            yield k, v

    def __setitem__(self, key, value):
        raise AssertionError("Options chain collection is read only")

    def __getitem__(self, item):
        if isinstance(item, datetime):
            return self._chains[item]
        elif isinstance(item, date):
            dt = datetime.combine(item, datetime.min.time())
            return self._chains[dt]
        elif isinstance(item, (int, np.int32, np.int64)):
            expiration = self._expirations[item]
            return self._chains[expiration]
        else:
            raise ValueError('Unexpected item type, must be float or int')

    def __repr__(self):
        exp_str = ""

        for i, exp in enumerate(self.expirations):
            exp_str += '{0}: {1}\n'.format(i, exp.date())
        return exp_str