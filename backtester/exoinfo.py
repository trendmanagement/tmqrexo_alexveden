from backtester import matlab
import pandas as pd


class EXOInfo(object):
    def __init__(self, data, exo_info):
        self.data = data
        self.exo_info = exo_info

    @classmethod
    def from_matfile(cls, filename):
        data, exo_info = matlab.loaddata(filename)
        return cls(data, exo_info)

    def margin(self):
        return pd.Series(self.exo_info['margin'], index=self.data.exo.index)

    def exo_name(self):
        underlying = self.exo_info['underlying']
        exoname = self.exo_info['name']
        return '{0}_{1}_EXO'.format(underlying, exoname)

    def exo_price_index(self):
        """
        Cumulative dollar values index of EXO price
        :return:
        """
        return self.data['exo'].diff().cumsum()
