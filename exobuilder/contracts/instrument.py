from exobuilder.contracts.futureschain import FuturesChain

class Instrument(object):
    """
    Underlying instrument class
    """
    def __init__(self, symbol, date, futures_limit, assetindex):
        """
        Initialize instrument class
        :param symbol: ticker of instrument in DB
        :param date: current calculation date
        :param assetindex: asset index instrument
        :param futures_limit: futures expirations limit for instrument in FuturesChains
        """
        self.assetindex = assetindex
        self.date = date
        self._datadic = assetindex.get_instrument_info(symbol)
        self.futures_limit = futures_limit
        self._futures_chain = None

    @property
    def dbid(self):
        return self._datadic['idinstrument']

    @property
    def name(self):
        return self._datadic['symbol']

    @property
    def symbol(self):
        return self._datadic['symbol']

    @property
    def futures(self):
        """
        Futures chains accessor
        :return:
        """
        if self._futures_chain is None:
            self._futures_chain = FuturesChain(self)

        return self._futures_chain
