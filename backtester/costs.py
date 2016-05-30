import pandas as pd


class CostsManagerZeroCosts(object):
    def __init__(self, exo_info, costs_context):
        self.exo_info = exo_info
        self.context = costs_context

    def get_costs(self, price):
        """
        Returns transactions costs vector for EXO
        :param price:
        :return:
        """
        return pd.Series(0, index=price.index)

