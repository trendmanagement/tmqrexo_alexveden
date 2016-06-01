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

    def _backtest_picked_swarm(self, filtered_swarm):
        swarm, swarm_stats, swarm_inposition = self.strategy.run_swarm(filtered_swarm)
        return swarm, swarm_inposition


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
        # Calculating global filter function if available
        #
        if 'global_filter_function' in swarm_settings:
            gf_func = swarm_settings['global_filter_function']
            params = None
            if 'global_filter_params' in swarm_settings:
                params = swarm_settings['global_filter_params']
            # Calculating global filter on Avg swarm equity line
            avg_swarm_equity = self.swarm_avg
            self.global_filter, self.global_filter_data = gf_func(avg_swarm_equity, params)

        #
        #   Ranking each swarm member's equity
        #
        ranks = self.swarm.apply(lambda x: rankerfunc(x, self.rebalancetime)).rank(axis=1, pct=True)

        is_picked_df = pd.DataFrame(0, index=self.swarm.index, columns=self.swarm.columns, dtype=np.int8)
        nbest = None

        for i in range(len(self.rebalancetime)):
            if i < 100:
                continue

            # Applying global trades filter
            if self.global_filter is not None:
                # If global filter is True on current day we filter all picks
                if not self.global_filter.values[i]:
                    continue

            if self.rebalancetime[i]:
                # Select N best ranked systems to trade
                nbest = (ranks.iloc[i].rank(pct=True, na_option='top')*100).sort_values()

                # Filter early trades
                if nbest.sum() == 0:
                    nbest[:] = 0
                    continue
                nbest = nbest.astype(np.uint8)

                # Flagging picked trading systems
                nbest[-nSystems:] = 1
                nbest[:-nSystems] = 0
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
        filered_swarm = is_picked_df[picked_swarms_cols]


        self.swarm_picked, self.swarm_picked_inposition = self._backtest_picked_swarm(filered_swarm)
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