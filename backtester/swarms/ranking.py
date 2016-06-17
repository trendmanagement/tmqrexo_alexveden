
import numpy as np
import pandas as pd


class SwarmRanker(object):
    @staticmethod
    def highestreturns_14days(eqty, rebalance_time):
        '''
        Ranking function
        Calculate last 14 days equity returns, excluding out-of-market time
        :param eqty: Swarm member equity
        :param rebalance_time: rebalance time
        :return: Series of metric which is used in ranking for swarm members
        '''
        return eqty.diff(periods=14)

    @staticmethod
    def highestreturns_max_sharpe(eqty, rebalance_time):
        '''
        Sharp based ranking function
        :param eqty: Swarm member equity
        :param rebalance_time: rebalance time
        :return: Series of metric which is used in ranking for swarm members
        '''
        raise Exception("Obsolete must be rewritten to handle DataFrame")
        chg = eqty.diff(periods=14)

        sharpe = chg.rolling(200).mean() / chg.rolling(200).std()

        return pd.Series(sharpe*100, index=eqty.index)

    @staticmethod
    def highestreturns_14days_with_slopefilter(eqty, rebalance_time):
        '''
        Ranking function
        Calculate last 14 days equity returns, excluding out-of-market time
        :param eqty: Swarm member equity
        :param rebalance_time: rebalance time
        :return: Series of metric which is used in ranking for swarm members
        '''
        q = eqty.rank(axis=1, pct=True)

        diff14 = eqty.diff(periods=14)
        ma90 = eqty.apply(lambda x: x.rolling(90).mean())

        rank = diff14
        # Filter all members with negative returns in 30 or 90 days
        rank[(eqty < ma90) | (ma90-ma90.shift(1) <= 0) | (eqty - eqty.shift(90) <= 0) | (q < 0.9)] = 0
        return rank
