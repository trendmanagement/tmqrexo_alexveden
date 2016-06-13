import numpy as np
import pandas as pd
from backtester.exoinfo import EXOInfo
import pickle


class SwarmManager(object):
    """
    Swarm picking algorithms class
    """
    def __init__(self, context=None):
        """
        Initialize picking engine with context
        :param context: dict(), strategy setting context
        :return:
        """
        self.context = context
        self.global_filter = None
        self.rebalancetime = None

    @staticmethod
    def get_average_swarm(swarm):
        """
        Returns swarm.diff().mean(axis=1).cumsum()

        :param swarm:
        :return:
        """
        eq_changes = swarm.diff()
        return eq_changes.mean(axis=1).cumsum()

    def check_context(self):
        """
        Checks context dict settings integrity
        :return:
        """

        # Check base strategy settings
        if 'strategy' not in self.context:
            raise ValueError('"strategy" settings not found')
        if 'class' not in self.context['strategy']:
            raise ValueError('"class" settings not found in "strategy" settings')

        # Check swarm specific setting
        if 'swarm' not in self.context:
            raise ValueError('"swarm" settings not found')
        swarm_settings = self.context['swarm']
        if 'members_count' not in swarm_settings:
            raise ValueError('"members_count" not found in swarm settings')
        if 'ranking_function' not in swarm_settings:
            raise ValueError('"ranking_function" not found in swarm settings')
        if 'rebalance_time_function' not in swarm_settings:
            raise ValueError('"rebalance_time_function" not found in swarm settings')

    def run_swarm(self):
        strategy_settings = self.context['strategy']

        # Initialize strategy class
        self.strategy = strategy_settings['class'](self.context)

        # Run strategy swarm
        self.swarm, self.swarm_stats, self.swarm_inposition = self.strategy.run_swarm()
        #
        # Average swarm multiplied by members_count
        #   for reproduce comparable results 'picked_swarm' vs 'avg_swarm'
        self.swarm_avg = SwarmManager.get_average_swarm(self.swarm) * self.context['swarm']['members_count']

    def _backtest_picked_swarm(self, filtered_swarm, filtered_swarm_equity):
        swarm, swarm_stats, swarm_inposition = self.strategy.run_swarm(filtered_swarm, filtered_swarm_equity)
        return swarm, swarm_inposition

    def _get_nbest(self, ranked_results, nsystems):
        # Select N best ranked systems to trade
        nbest = ranked_results.sort_values()


        results = pd.Series(0, index=nbest.index, dtype=np.int8)

        nanless_nbest = nbest[nbest > 0].dropna()

        #
        # Every nbest member value is NaN
        # Not enough data or something wrong with ranked_results
        if len(nanless_nbest) == 0:
            return results

        # Flagging picked trading systems
        results[nanless_nbest[-nsystems:].index] = 1
        return results

    def pick(self):
        """
        Backtesting and swarm picking routine
        :param swarm:
        :return:
        """

        self.check_context()

        swarm_settings = self.context['swarm']
        nSystems = swarm_settings['members_count']
        rankerfunc = swarm_settings['ranking_function']
        self.rebalancetime = swarm_settings['rebalance_time_function'](self.swarm)


        #
        #   Ranking each swarm member's equity
        #
        ranks = self.swarm.apply(lambda x: rankerfunc(x, self.rebalancetime))

        is_picked_df = pd.DataFrame(0, index=self.swarm.index, columns=self.swarm.columns, dtype=np.int8)
        nbest = None

        for i in range(len(self.rebalancetime)):
            if i < 100:
                continue

            # == True - to avoid NaN values to pass condition
            if self.rebalancetime[i] == True:
                nbest = self._get_nbest(ranks.iloc[i], nSystems)
                is_picked_df.iloc[i] = nbest
            else:
                # Flag last picked swarm members until new self.rebalancetime
                if nbest is not None:
                    is_picked_df.iloc[i] = nbest

        #
        #   Filtering unused swarm members
        #
        def filt_func(x):
            if x.sum() > 0:
                return 1
            else:
                return np.nan
        picked_swarms_cols = is_picked_df.apply(filt_func).dropna().index
        filtered_swarm = is_picked_df[picked_swarms_cols]

        #
        # Calculating swarm equity for picked global filter
        #
        diff_sw = self.swarm.diff()
        # is_picked_df.shift(1) - to avoid entry price backtest bug
        filtered_equity = diff_sw[is_picked_df.shift(1) == 1].sum(axis=1).cumsum()

        self.swarm_picked, self.swarm_picked_inposition = self._backtest_picked_swarm(filtered_swarm, filtered_equity)
        self.swarm_picked_margin = self.swarm_picked_inposition.sum(axis=1) * self.strategy.exoinfo.margin()
        #return self.swarm_picked

    def get_swarm_name(self):
        """
        Return swarm manager human-readable name
        Underlying_EXOName_Strategy_Direction
        :return:
        """
        underlying = self.strategy.exoinfo.exo_info['underlying']
        exoname = self.strategy.exoinfo.exo_info['name']
        strategyname = self.strategy.name
        direction = 'Long' if self.strategy.direction == 1 else 'Short'

        return '{0}_{1}_{2}_{3}'.format(underlying, exoname, strategyname, direction)

    def save(self, filename=None):
        if filename is None:
            fn = self.get_swarm_name() + '.swm'
        else:
            fn = filename

        with open(fn, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)