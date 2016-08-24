import numpy as np
import pandas as pd
from backtester.exoinfo import EXOInfo
import pickle
import os
from collections import OrderedDict

def ranker_14days(swarm_slice, nsystems):
    result = []
    rank_info = []
    # Select required window for calculations
    ss = swarm_slice #.iloc[-100:, :]

    # Calculate 14-period equity returns and sort values
    last_diff = ss.diff(periods=14).iloc[-1, :].sort_values(ascending=False).dropna()

    # Pick best nsystems
    best = last_diff[:nsystems]

    for k, v in best.items():
        if not np.isnan(v) and v > 0:
            result.append(k)
            rank_info.append({'rank_value': v})

    return result, rank_info

class Swarm:
    def __init__(self, context):
        """
        Initialize picking engine with context
        :param context: dict(), strategy setting context
        :return:
        """
        self.context = context
        self.global_filter = None
        self.rebalancetime = None
        self.swarm_stats = None


        strategy_settings = self.context['strategy']
        # Initialize strategy class
        self.strategy = strategy_settings['class'](self.context)

    @staticmethod
    def get_average_swarm(swarm):
        """
        Returns swarm.diff().mean(axis=1).cumsum()

        :param swarm:
        :return:
        """
        eq_changes = swarm.diff()
        return eq_changes.mean(axis=1).cumsum()

    def run_swarm(self):
        # Run strategy swarm
        self.swarm, self.swarm_stats, self.swarm_inposition = self.strategy.run_swarm_backtest()
        #
        # Average swarm multiplied by members_count
        #   for reproduce comparable results 'picked_swarm' vs 'avg_swarm'
        self.swarm_avg = self.get_average_swarm(self.swarm) * self.context['swarm']['members_count']


    def pick(self):
        """
        Backtesting and swarm picking routine
        :param swarm:
        :return:
        """

        swarm_settings = self.context['swarm']
        nSystems = swarm_settings['members_count']
        rankerfunc = swarm_settings['ranking_function']
        rankerparams = None
        if 'ranking_params' in swarm_settings:
            rankerparams = swarm_settings['ranking_params']
        self.rebalancetime = swarm_settings['rebalance_time_function'](self.swarm)

        picked_swarm_equity = np.zeros((len(self.swarm), nSystems))
        picked_swarm_inposition = np.zeros((len(self.swarm), nSystems))
        swarm_members = None
        rebalance_info = OrderedDict()

        for i in range(1, len(self.rebalancetime)):
            if swarm_members is not None and len(swarm_members) > 0:
                # Comment:
                # - get swarm / filter it by picked members columns
                # - Calculate diff() to previous equity values
                # NB this is matrix operation!
                last_swm_eq_change = self.swarm[swarm_members].iloc[i-1:i+1].diff().values[-1]

                # - Add swarm's equity change to picked swarm equity
                # NB this is matrix operation!
                picked_swarm_equity[i] = picked_swarm_equity[i-1] + last_swm_eq_change

                # Store picked in position data
                picked_swarm_inposition[i] = self.swarm_inposition[swarm_members].iloc[i].values
            else:
                # NB this is matrix operation!
                picked_swarm_equity[i] = picked_swarm_equity[i - 1]

            # == True - to avoid NaN values to pass condition
            if self.rebalancetime[i-1] == True:
                # To avoid future referencing in ranking functions use slicing
                swm_slice = self.swarm.iloc[:i, :]

                # Pick new ranked swarm members
                swarm_members, rank_info = ranker_14days(swm_slice, nSystems)
                #swarm_members, rank_info = rankerfunc(swm_slice, nSystems)

                rebalance_info[self.swarm.index[i]] = {
                    'rebalance_date': self.swarm.index[i],
                    'best_members': swarm_members,
                    'rank_info': rank_info
                }

        self.swarm_picked = pd.DataFrame(picked_swarm_equity, self.swarm.index)
        self.swarm_picked_inposition = pd.DataFrame(picked_swarm_inposition, self.swarm.index)
        self.rebalance_info = rebalance_info



