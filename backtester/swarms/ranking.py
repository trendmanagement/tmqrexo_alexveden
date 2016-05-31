
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


        """
        result = np.full_like(eqty, np.nan)
        for i in range(len(eqty)):
            # Skip first 30 days
            if i < 100:
                continue

            if not rebalance_time[i]:
                continue

            # Skip periods without trades
            e = np.unique(eqty[i-90:i+1])
            e_cnt = len(e)
            if e_cnt < 15:
                result[i] = np.nan
                continue
            # Recalculate last 14 period returns
            result[i] = e[-1] - e[-14]
        """

        return pd.Series(eqty.diff(periods=14), index=eqty.index)

    @staticmethod
    def highestreturns_max_sharpe(eqty, rebalance_time):
        '''
        Sharp based ranking function
        :param eqty: Swarm member equity
        :param rebalance_time: rebalance time
        :return: Series of metric which is used in ranking for swarm members
        '''

        chg = eqty.diff(periods=14)
        sharpe = chg.rolling(200).mean() / chg.rolling(200).std()

        return pd.Series(sharpe*100, index=eqty.index)