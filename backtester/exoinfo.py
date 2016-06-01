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
