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


class StrategyBollingerBands(StrategyBase):
    name = 'BolllingerBands'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)


    def calc_entry_rules(self, bb_period, bb_k, rules_index):

        df = pd.DataFrame()

        df = self.data
        if rules_index >= 14:
            
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

            df['bb_multiperiod_%b'] = (df.exo - df['bb_multiperiod_lowerband']) / (
                                        df['bb_multiperiod_upperband'] - df['bb_multiperiod_lowerband'])

            df['bb_multiperiod_width'] = (df['bb_multiperiod_upperband'] - df['bb_multiperiod_lowerband'])
        
        if rules_index <= 13:
            bb_period = bb_period
            bb_k = bb_k
            df['bb_central_line'] = df.exo.rolling(bb_period).mean()
            df['bb_upperband'] = df.bb_central_line + (bb_k * df.bb_central_line.rolling(bb_period).std())
            df['bb_lowerband'] = df.bb_central_line - (bb_k * df.bb_central_line.rolling(bb_period).std())

            df['bb_%b'] = (df.exo - df['bb_lowerband']) / (df['bb_upperband'] - df['bb_lowerband'])
            df['bb_width'] = (df['bb_upperband'] - df['bb_lowerband'])

        # Trend 0:5
        # Vola breakout 5:10
        # High vola(BBands width percent rank > 80-90) 10:15
        # %B rules 15:26
        if rules_index == 0:
            up_trend = (((df.exo - df.bb_upperband).rolling(10).median()) <= (df.exo - df.bb_upperband))
            
            return up_trend
        
        if rules_index == 1:
            down_trend = (df.bb_lowerband - df.exo).rolling(10).median() <= (df.bb_lowerband - df.exo)
            
            return down_trend
        
        if rules_index == 2:
            bb_width_pctrank_less_20 = df.bb_width.rank(pct=True) <= 0.2
            
            return bb_width_pctrank_less_20
        
        if rules_index == 3:
            bb_width_pctrank_less_10 = df.bb_width.rank(pct=True) <= 0.1
            
            return bb_width_pctrank_less_10
        
        if rules_index == 4:
            bb_width_pctrank_more_80 = df.bb_width.rank(pct=True) >= 0.8
            
            return bb_width_pctrank_more_80
        
        if rules_index == 5:
            bb_width_pctrank_more_90 = df.bb_width.rank(pct=True) >= 0.9
            
            return bb_width_pctrank_more_90
        
        if rules_index == 6:
            bb_width_pctrank_more_50 = df.bb_width.rank(pct=True) >= 0.5
            
            return bb_width_pctrank_more_50
        
        if rules_index == 7:
            bb_width_pctrank_less_50 = df.bb_width.rank(pct=True) <= 0.5
            
            return bb_width_pctrank_less_50
        
        if rules_index == 8:
            bb_pctb_pctrank_less_20 = df['bb_%b'].rank(pct=True) <= 0.2
            
            return bb_pctb_pctrank_less_20
        
        if rules_index == 9:
            bb_pctb_pctrank_less_10 = df['bb_%b'].rank(pct=True) <= 0.1
            
            return bb_pctb_pctrank_less_10
            
        if rules_index == 10:
            bb_pctb_pctrank_more_80 = df['bb_%b'].rank(pct=True) >= 0.8
            
            return bb_pctb_pctrank_more_80
        
        if rules_index == 11:
            bb_pctb_pctrank_more_90 = df['bb_%b'].rank(pct=True) <= 0.9
            
            return bb_pctb_pctrank_more_90
        
        if rules_index == 12:
            bb_pctb_pctrank_more_50 = df['bb_%b'].rank(pct=True) >= 0.5
            
            return bb_pctb_pctrank_more_50
        
        if rules_index == 13:
            bb_pctb_pctrank_less_50 = df['bb_%b'].rank(pct=True) <= 0.5
            
            return bb_pctb_pctrank_less_50
        
        if rules_index == 14:
            multiperiod_up_trend = ((df.exo - df.bb_multiperiod_upperband).rolling(10).median()) <= (
                                df.exo - df.bb_multiperiod_upperband)
            
            return multiperiod_up_trend
        
        if rules_index == 15:
            multiperiod_down_trend = (df.bb_multiperiod_lowerband - df.exo).rolling(10).median() <= (
                                    df.bb_multiperiod_lowerband - df.exo)
            
            return multiperiod_down_trend
        
        if rules_index == 16:
            bb_multiperiod_width_pctrank_less_20 = df.bb_multiperiod_width.rank(pct=True) <= 0.2
            
            return bb_multiperiod_width_pctrank_less_20
        
        if rules_index == 17:
            bb_multiperiod_width_pctrank_less_10 = df.bb_multiperiod_width.rank(pct=True) <= 0.1
            
            return bb_multiperiod_width_pctrank_less_10
        
        if rules_index == 18:
            bb_multiperiod_width_pctrank_more_80 = df.bb_multiperiod_width.rank(pct=True) >= 0.8
            
            return bb_multiperiod_width_pctrank_more_80
        
        if rules_index == 19:
            bb_multiperiod_width_pctrank_more_90 = df.bb_multiperiod_width.rank(pct=True) <= 0.9
            
            return bb_multiperiod_width_pctrank_more_90
        
        if rules_index == 20:
            bb_multiperiod_width_pctrank_more_50 = df.bb_multiperiod_width.rank(pct=True) >= 0.5
            
            return bb_multiperiod_width_pctrank_more_50
        
        if rules_index == 21:
            bb_multiperiod_width_pctrank_less_50 = df.bb_multiperiod_width.rank(pct=True) <= 0.5
            
            return bb_multiperiod_width_pctrank_less_50
        
        if rules_index == 22:
            bb_multiperiod_pctb_pctrank_less_20 = df['bb_multiperiod_%b'].rank(pct=True) <= 0.2
            
            return bb_multiperiod_pctb_pctrank_less_20
        
        if rules_index == 23:
            bb_multiperiod_pctb_pctrank_less_10 = df['bb_multiperiod_%b'].rank(pct=True) <= 0.1
            
            return bb_multiperiod_pctb_pctrank_less_10
        
        if rules_index == 24:
            bb_multiperiod_pctb_pctrank_more_80 = df['bb_multiperiod_%b'].rank(pct=True) >= 0.8
            
            return bb_multiperiod_pctb_pctrank_more_80
        
        if rules_index == 25:
            bb_multiperiod_pctb_pctrank_more_90 = df['bb_multiperiod_%b'].rank(pct=True) <= 0.9
            
            return bb_multiperiod_pctb_pctrank_more_90
        
        if rules_index == 26:
            bb_multiperiod_pctb_pctrank_more_50 = df['bb_multiperiod_%b'].rank(pct=True) >= 0.5
            
            return bb_multiperiod_pctb_pctrank_more_50
        
        if rules_index == 27:
            bb_multiperiod_pctb_pctrank_less_50 = df['bb_multiperiod_%b'].rank(pct=True) <= 0.5
            
            return bb_multiperiod_pctb_pctrank_less_50
        

        if rules_index > 27:
            raise ValueError('Rules index parameter must be in range of 0-27')
            
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


        # Median based trailing stop
        trailing_stop = px.rolling(period_median).median().shift(1)

        # Enry/exit rules
        entry_rule = self.calc_entry_rules(bb_period, bb_k, rules_index)

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
    #data.plot()

