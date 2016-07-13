from exobuilder.contracts.futurecontract import FutureContract
from datetime import date, datetime

class FuturesChain(object):
    def __init__(self, instrument):
        """
        Futures chains management class
        :param instrument: Instrument class instance
        """
        self.instrument = instrument
        self._data = self.instrument.assetindex.get_futures_list(self.instrument.date, self.instrument, self.instrument.futures_limit)
        self.contracts = []
        for f in self._data:
            self.contracts.append(FutureContract(f, self.instrument))

    @property
    def count(self):
        return len(self._data)

    @property
    def expirations(self):
        return [x.expiration for x in self.contracts]

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        if type(key) is datetime:
            # Finding future contract by datetime
            for c in self.contracts:
                if c.expiration == key:
                    return c
        elif type(key) is date:
            # Finding future contract by date
            for c in self.contracts:
                if c.expiration.date() == key:
                    return c

        # Finding future contract by strike offset from now
        return self.contracts[key]

    def __iter__(self):
        return self.contracts.__iter__()

    def items(self):
        for c in self.contracts:
            yield c.expiration, c

    def __setitem__(self, key, value):
        raise AssertionError("Futures chain collection is read only")

    def __str__(self):
        return str(self.contracts)

    def __repr__(self):
        sbuf = ''
        for i, c in enumerate(self.contracts):
            sbuf += '{0}: {1}\n'.format(i, c)
        return sbuf

