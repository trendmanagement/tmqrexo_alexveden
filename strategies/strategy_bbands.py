# coding: utf-8

# In[2]:

import sys, os

sys.path.append('..')
from backtester import matlab, backtester
from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam

import pandas as pd
import numpy as np
import scipy


class StrategyBolingerBands(StrategyBase):
    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

        # Define system's name
        self.name = 'BolingerBands'

        self.check_context()

        # Define optimized params
        self.opts = strategy_context['strategy']['opt_params']

    def check_context(self):
        #
        # Do strategy specific checks
        #
        pass

    def calc_entry_rules(self, bb_period, bb_k):

        df = pd.DataFrame()

        df = self.data

        for i in range(10, 100, 10):
            bb_period = i
            bb_k = 2
            df['bb_central_line' + str(i)] = df.exo.rolling(bb_period).mean()
            df['bb_upperband' + str(i)] = df['bb_central_line' + str(i)] + (
            bb_k * df['bb_central_line' + str(i)].rolling(bb_period).std())
            df['bb_lowerband' + str(i)] = df['bb_central_line' + str(i)] - (
            bb_k * df['bb_central_line' + str(i)].rolling(bb_period).std())

        df['bb_multiperiod_central_line'] = df.filter(like='centr').mean(axis=1)
        df['bb_multiperiod_upperband'] = df.filter(like='upper').mean(axis=1)
        df['bb_multiperiod_lowerband'] = df.filter(like='lower').mean(axis=1)

        bb_period = bb_period
        bb_k = bb_k
        df['bb_central_line'] = df.exo.rolling(bb_period).mean()
        df['bb_upperband'] = df.bb_central_line + (bb_k * df.bb_central_line.rolling(bb_period).std())
        df['bb_lowerband'] = df.bb_central_line - (bb_k * df.bb_central_line.rolling(bb_period).std())

        df['bb_%b'] = (df.exo - df['bb_lowerband']) / (df['bb_upperband'] - df['bb_lowerband'])
        df['bb_width'] = (df['bb_upperband'] - df['bb_lowerband'])

        df['bb_multiperiod_%b'] = (df.exo - df['bb_multiperiod_lowerband']) / (
                                    df['bb_multiperiod_upperband'] - df['bb_multiperiod_lowerband'])

        df['bb_multiperiod_width'] = (df['bb_multiperiod_upperband'] - df['bb_multiperiod_lowerband'])




        up_trend = (((df.exo - df.bb_upperband).rolling(10).median()) <= (df.exo - df.bb_upperband))

        down_trend = (df.bb_lowerband - df.exo).rolling(10).median() <= (df.bb_lowerband - df.exo)

        bb_width_pctrank_less_20 = df.bb_width.rank(pct=True) <= 0.2
        bb_width_pctrank_less_10 = df.bb_width.rank(pct=True) <= 0.1

        bb_width_pctrank_more_80 = df.bb_width.rank(pct=True) >= 0.8
        bb_width_pctrank_more_90 = df.bb_width.rank(pct=True) <= 0.9

        bb_width_pctrank_more_50 = df.bb_width.rank(pct=True) >= 0.5
        bb_width_pctrank_less_50 = df.bb_width.rank(pct=True) <= 0.5

        bb_pctb_pctrank_less_20 = df['bb_%b'].rank(pct=True) <= 0.2
        bb_pctb_pctrank_less_10 = df['bb_%b'].rank(pct=True) <= 0.1

        bb_pctb_pctrank_more_80 = df['bb_%b'].rank(pct=True) >= 0.8
        bb_pctb_pctrank_more_90 = df['bb_%b'].rank(pct=True) <= 0.9

        bb_pctb_pctrank_more_50 = df['bb_%b'].rank(pct=True) >= 0.5
        bb_pctb_pctrank_less_50 = df['bb_%b'].rank(pct=True) <= 0.5

        multiperiod_up_trend = ((df.exo - df.bb_multiperiod_upperband).rolling(10).median()) <= (
                                df.exo - df.bb_multiperiod_upperband)

        multiperiod_down_trend = (df.bb_multiperiod_lowerband - df.exo).rolling(10).median() <= (
                                    df.bb_multiperiod_lowerband - df.exo)

        bb_multiperiod_width_pctrank_less_20 = df.bb_multiperiod_width.rank(pct=True) <= 0.2
        bb_multiperiod_width_pctrank_less_10 = df.bb_multiperiod_width.rank(pct=True) <= 0.1

        bb_multiperiod_width_pctrank_more_80 = df.bb_multiperiod_width.rank(pct=True) >= 0.8
        bb_multiperiod_width_pctrank_more_90 = df.bb_multiperiod_width.rank(pct=True) <= 0.9

        bb_multiperiod_width_pctrank_more_50 = df.bb_multiperiod_width.rank(pct=True) >= 0.5
        bb_multiperiod_width_pctrank_less_50 = df.bb_multiperiod_width.rank(pct=True) <= 0.5

        bb_multiperiod_pctb_pctrank_less_20 = df['bb_multiperiod_%b'].rank(pct=True) <= 0.2
        bb_multiperiod_pctb_pctrank_less_10 = df['bb_multiperiod_%b'].rank(pct=True) <= 0.1

        bb_multiperiod_pctb_pctrank_more_80 = df['bb_multiperiod_%b'].rank(pct=True) >= 0.8
        bb_multiperiod_pctb_pctrank_more_90 = df['bb_multiperiod_%b'].rank(pct=True) <= 0.9

        bb_multiperiod_pctb_pctrank_more_50 = df['bb_multiperiod_%b'].rank(pct=True) >= 0.5
        bb_multiperiod_pctb_pctrank_less_50 = df['bb_multiperiod_%b'].rank(pct=True) <= 0.5

        bb_multiperiod_pctb_up_direction = (df['bb_multiperiod_%b'].rank(pct=True).rolling(10).mean() >=
                                            df['bb_multiperiod_%b'].rank(pct=True).rolling(10).mean().rolling(
                                                10).median())

        bb_multiperiod_pctb_down_direction = (df['bb_multiperiod_%b'].rank(pct=True).rolling(10).mean() <=
                                              df['bb_multiperiod_%b'].rank(pct=True).rolling(10).mean().rolling(
                                                  10).median())

        return up_trend, down_trend, bb_width_pctrank_less_20, bb_width_pctrank_less_10, bb_width_pctrank_more_80,\
        bb_width_pctrank_more_90, bb_width_pctrank_more_50, bb_width_pctrank_less_50, multiperiod_up_trend, \
        multiperiod_down_trend, bb_multiperiod_width_pctrank_less_20, bb_multiperiod_width_pctrank_less_10,\
        bb_multiperiod_width_pctrank_more_80, bb_multiperiod_width_pctrank_more_90, bb_multiperiod_width_pctrank_more_50,\
        bb_multiperiod_width_pctrank_less_50, bb_multiperiod_pctb_pctrank_less_20, bb_multiperiod_pctb_pctrank_less_10,\
        bb_multiperiod_pctb_pctrank_more_80, bb_multiperiod_pctb_pctrank_more_90, bb_multiperiod_pctb_pctrank_more_50,\
        bb_multiperiod_pctb_pctrank_less_50, bb_multiperiod_pctb_up_direction, bb_multiperiod_pctb_down_direction

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
            direction, bb_period, bb_k, rules_index, period_median = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, bb_period, bb_k, rules_index, period_median = params

        # Defining EXO price
        px = self.data.exo

        rules_list = self.calc_entry_rules(bb_period, bb_k)

        # Median based trailing stop
        trailing_stop = px.rolling(period_median).median().shift(1)

        # Enry/exit rules
        entry_rule = pd.Series(rules_list[rules_index])

        if direction == 1:
            exit_rule = (CrossDown(px, trailing_stop))  # Cross down for longs
        elif direction == -1 :
            exit_rule = (CrossUp(px, trailing_stop))  # Cross up for shorts, Cross down for longs



            #exit_rule = pd.Series(rules_list[exit_rules_index])
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


if __name__ == "__main__":
    #
    #   Run this code only from direct shell execution
    #
    # strategy = StrategyMACrossTrail()
    # equity, stats = strategy.calculate()

    # Do some work
    data, info = matlab.loaddata('../mat/strategy_270225.mat')
    data.plot()


# In[ ]:
