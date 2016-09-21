from exobuilder.contracts.futureschain import FuturesChain

class Instrument(object):
    """
    Underlying instrument class
    """
    def __init__(self, datasource, datadict, date, futures_limit, options_limit=0):
        """
        Initialize instrument class
        :param datasource: asset index instrument
        :param datadict: instrument data dict from AssetIndex
        :param date: current calculation date
        :param futures_limit: futures expirations limit for instrument in FuturesChains
        :param options_limit: max strikes per side in Options chains
        """
        self.datasource = datasource
        self.date = date
        self._datadic = datadict
        self.futures_limit = futures_limit
        self.options_limit = options_limit
        self._futures_chain = None


    @property
    def assetindex(self):
        return self.datasource.assetindex

    @property
    def dbid(self):
        return self._datadic['idinstrument']

    @property
    def name(self):
        return self._datadic['exchangesymbol']

    @property
    def symbol(self):
        return self._datadic['exchangesymbol']

    @property
    def point_value_futures(self):
        return 1.0 / self._datadic['ticksize'] * self._datadic['tickvalue']

    @property
    def point_value_options(self):
        return 1.0 / self._datadic['optionticksize'] * self._datadic['optiontickvalue']

    @property
    def futures(self):
        """
        Futures chains accessor
        :return:
        """
        if self._futures_chain is None:
            self._futures_chain = FuturesChain(self)

        return self._futures_chain
