from exobuilder.data.datasource import DataSourceBase


class DataSourceForTest(DataSourceBase):
    def __init__(self, assetindex, futures_limit, options_limit):
        super().__init__(assetindex, futures_limit, options_limit)

    def get_extra_data(self, key, date):
        if key == 'riskfreerate':
            return 0.255

    def get_option_data(self, dbid, date):
        if dbid == 11558454:
            return {"impliedvol": 0.356}

    def get_fut_data(self, dbid, date):
        return {'close': 2770.0}