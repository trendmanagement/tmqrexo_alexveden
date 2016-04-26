import numpy as np
import pandas as pd


class SwarmManager(object):
    """
    Swarm picking algorithms class
    """
    def __init__(self, rebalancetime, rankerfunc, positionsizing, context=None):
        """
        Initialize picking engine with context
        :param rebalancetime: Pandas Series object, boolean with equal to swarm index
        :param rankerfunc: Swarm ranking function
        :param positionsizing: instance of PositionSizing class
        :param context: dict(), Some ranking algorithm params
        :return:
        """
        self.rebalancetime = rebalancetime
        self.rankerfunc = rankerfunc
        self.context = context
        self.positionsizing = positionsizing

    @staticmethod
    def get_average_swarm(swarm):
        eq_changes = swarm.diff()
        return eq_changes.mean(axis=1).cumsum()


    def backtest(self, swarm, global_filter=None, rabalance_costs=None):

        if 'nsystems' not in self.context:
            raise ValueError('nsystems parameter must be in context dic()')

        nSystems = self.context['nsystems']

        #
        #   Ranking each swarm member's equity
        #
        ranks = swarm.apply(lambda x: self.rankerfunc(x, self.rebalancetime)).rank(axis=1, pct=True)

        is_picked_df = pd.DataFrame(False, index=swarm.index, columns=swarm.columns)
        nbest = None

        for i in range(len(self.rebalancetime)):
            if i < 100:
                continue

            # Applying global trades filter
            if global_filter is not None:
                # If global filter is True on current day we filter all picks
                if global_filter.values[i]:
                    continue

            if self.rebalancetime[i]:
                # Select N best ranked systems to trade
                nbest = ranks.iloc[i].sort_values()

                # Filter early trades
                if nbest.sum() == 0:
                    nbest[:] = False
                    continue

                # Flagging picked trading systems
                nbest[-nSystems:] = True
                nbest[:-nSystems] = False
                is_picked_df.iloc[i] = nbest

            else:
                # Flag last picked swarm members until new self.rebalancetime
                if nbest is not None:
                    is_picked_df.iloc[i] = nbest
        return is_picked_df


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

        result = np.full_like(eqty, np.nan)

        for i in range(len(eqty)):
            # Skip first 30 days
            if i < 100:
                continue

            if not rebalance_time[i]:
                continue

            # Skip periods without trades
            e = np.unique(eqty[i-90:i+1])
            if len(e) < 15:
                result[i] = np.nan
                continue
            # Recalculate last 14 period returns
            result[i] = e[len(e) - 1] - e[len(e) - 14]

        return pd.Series(result, index=eqty.index)