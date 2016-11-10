# coding: utf-8

# In[2]:

import sys

from backtester.analysis import *
from backtester.strategy import StrategyBase
import pandas as pd
import numpy as np




class StrategyMachineLearnedCompetitor(StrategyBase):
    name = 'MachineLearnedCompetitor'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

    def calc_entry_rules(self, rolling_window_period, pctrank_value):

        px = self.data.exo

        price_more_than_rel_str_pctrank = (px - px.rolling(rolling_window_period).mean()).rank(
            pct=True) >= pctrank_value

        price_less_than_rel_str_pctrank = (px - px.rolling(rolling_window_period).mean()).rank(
            pct=True) <= pctrank_value

        price_above_ma = px > px.rolling(rolling_window_period).mean()
        price_below_ma = px < px.rolling(rolling_window_period).mean()

        price_more_than_pricechange_skew_pctrank = (px.diff().rolling(rolling_window_period).skew().rank(
            pct=True)) >= pctrank_value

        price_less_than_pricechange_skew_pctrank = (px.diff().rolling(rolling_window_period).skew().rank(
            pct=True)) <= pctrank_value

        return price_more_than_rel_str_pctrank, price_less_than_rel_str_pctrank, price_above_ma, price_below_ma, \
               price_more_than_pricechange_skew_pctrank, price_less_than_pricechange_skew_pctrank

    def calculate(self, params=None, save_info=False):
        #
        #
        #  Params is a tripple like (50, 10, 15), where:
        #   50 - slow MA period
        #   10 - fast MA period
        #   15 - median period
        #
        #  On every iteration of swarming algorithm, parameter set will be different.
        #  For more information look inside: /notebooks/tmp/Swarming engine research.ipynb
        #

        if params is None:
            # Return default parameters
            direction, rolling_window_period, pctrank_value, rules_index, period_median = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, rolling_window_period, pctrank_value, rules_index, period_median = params

        # Defining EXO price
        px = self.data.exo

        rules_list = self.calc_entry_rules(rolling_window_period, pctrank_value)

        # Median based trailing stop
        trailing_stop = px.rolling(period_median).median().shift(1)

        # Enry/exit rules
        entry_rule = pd.Series(rules_list[rules_index])

        if direction == 1:
            exit_rule = (CrossDown(px, trailing_stop))  # Cross down for longs

        elif direction == -1:
            exit_rule = (CrossUp(px, trailing_stop))  # Cross up for shorts, Cross down for longs

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None
        if save_info:
            calc_info = {'trailing_stop': trailing_stop}

        return swarm_member_name, entry_rule, exit_rule, calc_info

