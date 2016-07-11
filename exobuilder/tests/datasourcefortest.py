from exobuilder.data.datasource import DataSourceBase


class DataSourceForTest(DataSourceBase):
    def __init__(self, assetindex, date, futures_limit, options_limit):
        super().__init__(assetindex, date, futures_limit, options_limit)