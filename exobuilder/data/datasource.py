from exobuilder.contracts.instrument import Instrument

class DataSourceBase(object):
    def __init__(self, assetindex, date, futures_limit, options_limit):
        self.assetindex = assetindex
        self.date = date
        self.futures_limit = futures_limit
        self.options_limit = options_limit


    def get_fut_data(self, dbid, date):
        raise NotImplementedError()

    def get_option_data(self, dbid, date):
        raise NotImplementedError()

    def get_extra_data(self, key, date):
        raise NotImplementedError()

    def __getitem__(self, item):
        return Instrument(self, item, self.date, self.futures_limit, self.options_limit)
