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


class StrategyRenkoPatterns(StrategyBase):
    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

        # Define system's name
        self.name = 'RenkoPatterns'

        self.check_context()

        # Define optimized params
        self.opts = strategy_context['strategy']['opt_params']

    def check_context(self):
        #
        # Do strategy specific checks
        #
        pass

    def calc_entry_rules(self, box_size):


        df = pd.DataFrame()
        df['close'] = self.data.exo
        
        box_size = box_size # OPT PARAM

        box_start = 0
        box_start_idx = None

        box_end = 0
        box_quantity = 0

        temp_l = []

        # Simple renko algorihtm


        # 
        for i in range(len(df)):
            if box_start == 0:
                box_start = df.close[i]

            else:
                box_start = box_start
                price_move = df.close[i] - box_start

                # First of all we need to set box size. 
                # Then calculate price movement. 
                # If price movement is more or equal than box size - renko bar(or bars) will be added

                if np.abs(price_move) >= box_size:

                    # After we calculate box_quantity(price move divided by box size)
                    # This number defines how much renko bars will be registred
                    box_quantity = np.int32(np.floor(np.abs(price_move / box_size)))
                    box_index = df.close.index[i]

                    for b in range(int(box_quantity)):
                    # Let say, index is 2015-01-01, box_start = 100, box_quantity = 3, box size = 10, price move > 0
                    # So renko bar 1 will have next parameters - 
                    # 1)index 2015-01-01
                    # 2)open = 100
                    # 3)close = 110(box_start + box_size)
                    # 4)type = up

                    # Next renko bar will have next parameters -
                    # 1)index 2015-01-01
                    # 2)open = 110(previous renko bar close)
                    # 3)close = 120(open + box_size)
                    # 4)type = up

                    # And so on..

                    # After all we adding renko bars dict to list and convert it to DF

                        if price_move > 0:
                            if box_end == 0:
                                d = {'date': box_index, 'open': box_start, 'close': box_start + box_size, 'type': 'up'}
                                box_end = d['close']
                                temp_l.append(d)

                            else:
                                d = {'date': box_index, 'open': box_end, 'close': box_end + box_size,
                                    'type': 'up'}

                                box_end = d['close']
                                temp_l.append(d)

                        if price_move < 0:
                            if box_end == 0:
                                d = {'date': box_index, 'open': box_start, 'close': box_start - box_size, 'type': 'down'}
                                box_end = d['close']
                                temp_l.append(d)

                            else:           
                                d = {'date': box_index, 'open': box_end, 'close': box_end - box_size, 
                                     'type': 'down'}

                                box_end = d['close']
                                temp_l.append(d)

                    box_start = df.close[i]

        renko_df = pd.DataFrame(temp_l)

        del temp_l

        high_l = []
        low_l = []
        for i in range(len(renko_df)):
            if renko_df.close[i] > renko_df.open[i]:
                high_l.append(renko_df.close[i])
                low_l.append(renko_df.open[i])

            if renko_df.close[i] < renko_df.open[i]:
                high_l.append(renko_df.open[i])
                low_l.append(renko_df.close[i])

        renko_df['low'] = low_l
        renko_df['high'] = high_l

        del low_l
        del high_l
        
        ## Defining peaks and falls
        # Peaks
        renko_peak = ((renko_df.type == 'down') & (renko_df.type.shift(1) == 'down') 
                  & (renko_df.type.shift(2) == 'up') & (renko_df.type.shift(3) == 'up'))

        renko_df['peak'] = renko_peak
        
        # Falls
        renko_fall = ((renko_df.type == 'up') & (renko_df.type.shift(1) == 'up') 
                  & (renko_df.type.shift(2) == 'down') & (renko_df.type.shift(3) == 'down'))

        renko_df['fall'] = renko_fall

        ## Flat and trend patterns
        renko_flat = (((renko_df.type == 'up') & (renko_df.type.shift(1) == 'down') 
                & (renko_df.type.shift(2) == 'up') & (renko_df.type.shift(3) == 'down')) | 
              ((renko_df.type == 'down') & (renko_df.type.shift(1) == 'up') & (renko_df.type.shift(2) == 'down') 
             & (renko_df.type.shift(3) == 'up')))

        renko_df['flat'] = renko_flat

        renko_trend_up = ((renko_df.type == 'up') & (renko_df.type.shift(1) == 'up') & (renko_df.type.shift(2) == 'up'))
        renko_trend_down = ((renko_df.type == 'down') & (renko_df.type.shift(1) == 'down') & (renko_df.type.shift(2) == 'down'))

        renko_df['trend_up'] = renko_trend_up
        renko_df['trend_down'] = renko_trend_down
        
        renko_small_double_top = ((renko_df.type == 'down') & (renko_df.type.shift(1) == 'down') & (renko_df.type.shift(2) == 'up')
                         & (renko_df.type.shift(3) == 'down') & (renko_df.type.shift(4) == 'up') & (renko_df.type.shift(5) == 'up'))

        renko_df['small_double_top'] = renko_small_double_top

        renko_small_double_bottom = ((renko_df.type == 'up') & (renko_df.type.shift(1) == 'up') & (renko_df.type.shift(2) == 'down')
                                 & (renko_df.type.shift(3) == 'up') & (renko_df.type.shift(4) == 'down') & (renko_df.type.shift(5) == 'down'))

        renko_df['small_double_bottom'] = renko_small_double_bottom

        renko_up_trend_correction = (
        (renko_df.type == 'up') & (renko_df.type.shift(1) == 'up') & (renko_df.type.shift(2) == 'down')
        & (renko_df.type.shift(3) == 'up') & (renko_df.type.shift(4) == 'up'))

        renko_df['up_trend_correction'] = renko_up_trend_correction

        renko_down_trend_correction = (
        (renko_df.type == 'down') & (renko_df.type.shift(1) == 'down') & (renko_df.type.shift(2) == 'up')
        & (renko_df.type.shift(3) == 'down') & (renko_df.type.shift(4) == 'down'))

        renko_df['down_trend_correction'] = renko_down_trend_correction

        ## Consecutive up/down brick count

        df = df.join(
            renko_df.set_index('date')[['peak', 'fall', 'flat', 'trend_up', 'trend_down', 'small_double_bottom',
                                        'small_double_top', 'up_trend_correction', 'down_trend_correction']])

        df = df.fillna(False)

        signals_df = self.data.join(df)

        return signals_df.peak == True, signals_df.fall == True, signals_df.flat == True, signals_df.trend_up == True, \
               signals_df.trend_down == True

        #return signals_df.peak == True, signals_df.fall == True, signals_df.flat == True, \
        #      signals_df.trend_up == True, signals_df.trend_down == True, signals_df.small_double_bottom == True, \
        #      signals_df.small_double_top == True, signals_df.up_trend_correction == True, \
        #      signals_df.down_trend_correction == True

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
            direction, box_size, rules_index, period_median = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, box_size, rules_index, period_median = params

        # Defining EXO price
        px = self.data.exo

        rules_list = self.calc_entry_rules(box_size)

        # Median based trailing stop
        trailing_stop = px.rolling(period_median).median().shift(1)

        # Enry/exit rules
        entry_rule = pd.Series(rules_list[rules_index])

        if direction == 1:
            exit_rule = (CrossDown(px, trailing_stop))  # Cross down for longs
            #exit_rule = pd.Series(rules_list[exit_rules_index])
        elif direction == -1:
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
