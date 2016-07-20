

class AssetIndexBase(object):
    def get_instrument_info(self, symbol):
        """
        Returns underlying instrument information
        :param symbol: underlying ticker name
        :return: dict of underlying metadata
        """
        raise NotImplementedError()

    def get_futures_list(self, date, instrument, limit):
        """
        Returns not expired futures contracts list on specific expiration
        :param date: datetime
        :param instrument: Instrument class instance to search
        :param limit: limit of expirations count
        :return: list of futures metadata dicts
        """
        raise NotImplementedError()

    def get_options_list(self, date, futurecontract):
        """
        Returns options metadate on specific date and FutureContract
        :param date: datetime
        :param futurecontract: FutureContract class
        :return: list of options metadata dicts
        """
        raise NotImplementedError()

    def get_instrument(self, dbid):
        raise NotImplementedError()

    def get_future_contract(self, dbid):
        raise NotImplementedError()

    def get_option_contract(self, dbid):
        raise NotImplementedError()
