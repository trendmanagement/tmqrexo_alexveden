import numpy as np


class PutCallPair(object):
    def __init__(self):
        self._put = None
        self._call = None
        self._strike = np.nan
        self._expiration = None

    def addoption(self, option_contract):
        if option_contract.putorcall == 'P':
            if self._put is not None:
                raise ValueError('Put duplicate in PutCall pair')
            self._put = option_contract
        if option_contract.putorcall == 'C':
            if self._call is not None:
                raise ValueError('Call duplicate in PutCall pair')
            self._call = option_contract

        if np.isnan(self._strike):
            self._strike = option_contract.strike
        else:
            if self._strike != option_contract.strike:
                raise ValueError('Options have different strike prices')

        if self._expiration is None:
            self._expiration = option_contract.expiration
        else:
            if self._expiration != option_contract.expiration:
                raise ValueError('Options have different expiration dates')



    @property
    def strike(self):
        return self._strike

    @property
    def expiration(self):
        return self._expiration

    @property
    def C(self):
        return self._call

    @property
    def c(self):
        return self._call

    @property
    def call(self):
        return self._call

    @property
    def p(self):
        return self._put

    @property
    def P(self):
        return self._put

    @property
    def put(self):
        return self._put

    @property
    def underlying(self):
        if self._call is not None:
            return self._call.underlying
        if self._put is not None:
            return self._put.underlying

        return None

