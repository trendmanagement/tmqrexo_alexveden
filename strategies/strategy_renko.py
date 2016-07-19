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

    def calc_entry_rules(self, box_size, move_count, exit_on_peakfall_patterns):


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

        renko_df['renko_peak_price'] = renko_df.close[renko_df.peak.shift(-2) == True]
        renko_df.renko_peak_price = renko_df.renko_peak_price.shift(2)  # This needed for avoiding future reference problem

        # Falls
        renko_fall = ((renko_df.type == 'up') & (renko_df.type.shift(1) == 'up') 
                  & (renko_df.type.shift(2) == 'down') & (renko_df.type.shift(3) == 'down'))

        renko_df['fall'] = renko_fall

        renko_df['renko_fall_price'] = renko_df.close[renko_df.fall.shift(-2) == True]
        renko_df.renko_fall_price = renko_df.renko_fall_price.shift(
            2)  # This needed for avoiding future reference problem

        renko_df.renko_peak_price = renko_df.renko_peak_price.fillna(method='ffill')
        renko_df.renko_fall_price = renko_df.renko_fall_price.fillna(method='ffill')

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
        up_count = np.zeros_like(renko_df.index)
        up_counter = 0

        down_count = np.zeros_like(renko_df.index)
        down_counter = 0

        for i in range(len(renko_df.index)):
            if i > 0:

                if (renko_df.type[i] == 'up') & (renko_df.type[i - 1] == 'down'):
                    up_counter = 1
                    up_count[i] = up_counter

                elif (renko_df.type[i] == 'up') & (renko_df.type[i - 1] == 'up'):
                    up_counter += 1
                    up_count[i] = up_counter

                elif (renko_df.type[i] == 'down') & (renko_df.type[i - 1] == 'up'):
                    up_counter = 0
                    up_count[i] = up_counter

                else:
                    up_counter = 0
                    up_count[i] = up_counter

                if (renko_df.type[i] == 'down') & (renko_df.type[i - 1] == 'up'):
                    down_counter = 1
                    down_count[i] = down_counter

                elif (renko_df.type[i] == 'down') & (renko_df.type[i - 1] == 'down'):
                    down_counter += 1
                    down_count[i] = down_counter

                elif (renko_df.type[i] == 'up') & (renko_df.type[i - 1] == 'down'):
                    down_counter = 0
                    down_count[i] = down_counter

                else:
                    down_counter = 0
                    down_count[i] = down_counter

        renko_df['up_count'] = up_count
        renko_df['down_count'] = down_count

        # Peak/fall prices patterns
        ### Defining peak/fall price direction relative to previous peak/fall price

        renko_peak_df = renko_df[renko_df.peak == True]

        renko_peak_price_move = np.array([None] * len(renko_peak_df.type))
        # renko_peak_price_move = np.empty_like(renko_peak_df.type) # This code crashes the python...

        for i in range(len(renko_peak_df)):
            if i > 0:
                if renko_peak_df.renko_peak_price.values[i] > renko_peak_df.renko_peak_price.values[i - 1]:
                    renko_peak_price_move[i] = 'up'

                elif renko_peak_df.renko_peak_price.values[i] < renko_peak_df.renko_peak_price.values[i - 1]:
                    renko_peak_price_move[i] = 'down'

                elif renko_peak_df.renko_peak_price.values[i - 1] == renko_peak_df.renko_peak_price.values[i]:
                    renko_peak_price_move[i] = 'same'

        renko_df = renko_df.join(
            pd.Series(renko_peak_price_move, index=renko_peak_df.index, name='renko_peak_price_move').replace([None],
                                                                                                              np.NaN))

        del renko_peak_df

        renko_fall_df = renko_df[renko_df.fall == True]

        renko_fall_price_move = np.array([None] * len(renko_fall_df.type))

        for i in range(len(renko_fall_df)):
            if i > 0:
                if renko_fall_df.renko_fall_price.values[i] > renko_fall_df.renko_fall_price.values[i - 1]:
                    renko_fall_price_move[i] = 'up'

                elif renko_fall_df.renko_fall_price.values[i] < renko_fall_df.renko_fall_price.values[i - 1]:
                    renko_fall_price_move[i] = 'down'

                elif renko_fall_df.renko_fall_price.values[i - 1] == renko_fall_df.renko_fall_price.values[i]:
                    renko_fall_price_move[i] = 'same'

        renko_df = renko_df.join(
            pd.Series(renko_fall_price_move, index=renko_fall_df.index, name='renko_fall_price_move').replace([None],
                                                                                                              np.NaN))

        del renko_fall_df

        ## Patterns
        #### Peak
        #### Consecutive peak price movements count

        renko_peak_price_move_ser = renko_df.renko_peak_price_move.dropna()
        renko_peak_price_move_ser_prev = renko_df.renko_peak_price_move.dropna().shift(1)

        up_move_count = []
        up_move_counter = 0

        down_move_count = []
        down_move_counter = 0

        same_move_count = []
        same_move_counter = 0

        for i in renko_peak_price_move_ser.index:

            if i > 0:
                # Consec Up peak price movements
                if (renko_peak_price_move_ser[i] == 'up') & (renko_peak_price_move_ser_prev[i] != 'up'):
                    up_move_counter = 1
                    up_move_count.append(up_move_counter)

                elif (renko_peak_price_move_ser[i] == 'up') & (renko_peak_price_move_ser_prev[i] == 'up'):
                    up_move_counter += 1
                    up_move_count.append(up_move_counter)

                elif (renko_peak_price_move_ser[i] != 'up') & (renko_peak_price_move_ser_prev[i] == 'up'):
                    up_move_counter = 0
                    up_move_count.append(up_move_counter)

                elif (renko_peak_price_move_ser[i] != 'up') & (renko_peak_price_move_ser_prev[i] != 'up'):
                    up_move_counter = 0
                    up_move_count.append(up_move_counter)

                    # Consec down peak price movements
                if (renko_peak_price_move_ser[i] == 'down') & (renko_peak_price_move_ser_prev[i] != 'down'):
                    down_move_counter = 1
                    down_move_count.append(down_move_counter)

                elif (renko_peak_price_move_ser[i] == 'down') & (renko_peak_price_move_ser_prev[i] == 'down'):
                    down_move_counter += 1
                    down_move_count.append(down_move_counter)

                elif (renko_peak_price_move_ser[i] != 'down') & (renko_peak_price_move_ser_prev[i] == 'down'):
                    down_move_counter = 0
                    down_move_count.append(down_move_counter)

                elif (renko_peak_price_move_ser[i] != 'down') & (renko_peak_price_move_ser_prev[i] != 'down'):
                    down_move_counter = 0
                    down_move_count.append(down_move_counter)

                    # Consec same peak price movements
                if (renko_peak_price_move_ser[i] == 'same') & (renko_peak_price_move_ser_prev[i] != 'same'):
                    same_move_counter = 1
                    same_move_count.append(same_move_counter)

                elif (renko_peak_price_move_ser[i] == 'same') & (renko_peak_price_move_ser_prev[i] == 'same'):
                    same_move_counter += 1
                    same_move_count.append(same_move_counter)

                elif (renko_peak_price_move_ser[i] != 'same') & (renko_peak_price_move_ser_prev[i] == 'same'):
                    same_move_counter = 0
                    same_move_count.append(same_move_counter)

                elif (renko_peak_price_move_ser[i] != 'same') & (renko_peak_price_move_ser_prev[i] != 'same'):
                    same_move_counter = 0
                    same_move_count.append(same_move_counter)

        renko_df['renko_peak_price_up_move_count'] = pd.Series(up_move_count, index=renko_peak_price_move_ser.index,
                                                               name='renko_peak_price_up_move_count')

        renko_df['renko_peak_price_down_move_count'] = pd.Series(down_move_count, index=renko_peak_price_move_ser.index,
                                                                 name='renko_peak_price_down_move_count')

        renko_df['renko_peak_price_same_move_count'] = pd.Series(same_move_count, index=renko_peak_price_move_ser.index,
                                                                 name='renko_peak_price_same_move_count')

        #### Fall
        #### Consecutive peak price movements count

        renko_fall_price_move_ser = renko_df.renko_fall_price_move.dropna()
        renko_fall_price_move_ser_prev = renko_df.renko_fall_price_move.dropna().shift(1)

        up_move_count = []
        up_move_counter = 0

        down_move_count = []
        down_move_counter = 0

        same_move_count = []
        same_move_counter = 0

        for i in renko_fall_price_move_ser.index:

            if i > 0:
                # Consec Up fall price movements
                if (renko_fall_price_move_ser[i] == 'up') & (renko_fall_price_move_ser_prev[i] != 'up'):
                    up_move_counter = 1
                    up_move_count.append(up_move_counter)

                elif (renko_fall_price_move_ser[i] == 'up') & (renko_fall_price_move_ser_prev[i] == 'up'):
                    up_move_counter += 1
                    up_move_count.append(up_move_counter)

                elif (renko_fall_price_move_ser[i] != 'up') & (renko_fall_price_move_ser_prev[i] == 'up'):
                    up_move_counter = 0
                    up_move_count.append(up_move_counter)

                elif (renko_fall_price_move_ser[i] != 'up') & (renko_fall_price_move_ser_prev[i] != 'up'):
                    up_move_counter = 0
                    up_move_count.append(up_move_counter)

                    # Consec down fall price movements
                if (renko_fall_price_move_ser[i] == 'down') & (renko_fall_price_move_ser_prev[i] != 'down'):
                    down_move_counter = 1
                    down_move_count.append(down_move_counter)

                elif (renko_fall_price_move_ser[i] == 'down') & (renko_fall_price_move_ser_prev[i] == 'down'):
                    down_move_counter += 1
                    down_move_count.append(down_move_counter)

                elif (renko_fall_price_move_ser[i] != 'down') & (renko_fall_price_move_ser_prev[i] == 'down'):
                    down_move_counter = 0
                    down_move_count.append(down_move_counter)

                elif (renko_fall_price_move_ser[i] != 'down') & (renko_fall_price_move_ser_prev[i] != 'down'):
                    down_move_counter = 0
                    down_move_count.append(down_move_counter)

                    # Consec same fall price movements
                if (renko_fall_price_move_ser[i] == 'same') & (renko_fall_price_move_ser_prev[i] != 'same'):
                    same_move_counter = 1
                    same_move_count.append(same_move_counter)

                elif (renko_fall_price_move_ser[i] == 'same') & (renko_fall_price_move_ser_prev[i] == 'same'):
                    same_move_counter += 1
                    same_move_count.append(same_move_counter)

                elif (renko_fall_price_move_ser[i] != 'same') & (renko_fall_price_move_ser_prev[i] == 'same'):
                    same_move_counter = 0
                    same_move_count.append(same_move_counter)

                elif (renko_fall_price_move_ser[i] != 'same') & (renko_fall_price_move_ser_prev[i] != 'same'):
                    same_move_counter = 0
                    same_move_count.append(same_move_counter)

        renko_df['renko_fall_price_up_move_count'] = pd.Series(up_move_count, index=renko_fall_price_move_ser.index,
                                                               name='renko_fall_price_up_move_count')

        renko_df['renko_fall_price_down_move_count'] = pd.Series(down_move_count, index=renko_fall_price_move_ser.index,
                                                                 name='renko_fall_price_down_move_count')

        renko_df['renko_fall_price_same_move_count'] = pd.Series(same_move_count, index=renko_fall_price_move_ser.index,
                                                                 name='renko_fall_price_same_move_count')

        df = df.join(
            renko_df.set_index('date')[['peak', 'fall', 'flat', 'trend_up', 'trend_down', 'small_double_bottom',
                                        'small_double_top', 'up_trend_correction', 'down_trend_correction']])

        df = df.fillna(False)

        df = df.join(renko_df.set_index('date')[['renko_peak_price_move', 'renko_fall_price_move']])

        df = df.join(renko_df.set_index('date')[['up_count', 'down_count', 'renko_peak_price_up_move_count',
                                                 'renko_peak_price_down_move_count', 'renko_peak_price_same_move_count',
                                                 'renko_fall_price_up_move_count', 'renko_fall_price_down_move_count',
                                                 'renko_fall_price_same_move_count']])



        signals_df = self.data.join(df)

        return signals_df.peak == True, signals_df.fall == True, signals_df.flat == True, signals_df.trend_up == True, \
               signals_df.trend_down == True, signals_df.renko_peak_price_up_move_count == move_count, \
               signals_df.renko_peak_price_down_move_count == move_count, signals_df.renko_peak_price_same_move_count == move_count, \
               signals_df.renko_fall_price_up_move_count == move_count, signals_df.renko_fall_price_down_move_count == move_count, \
               signals_df.renko_peak_price_same_move_count == move_count








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
            direction, box_size, move_count, exit_on_patterns, exit_rules_index, rules_index, period_median = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, box_size, move_count, exit_on_patterns, exit_rules_index, rules_index, period_median = params

        # Defining EXO price
        px = self.data.exo

        rules_list = self.calc_entry_rules(box_size, move_count, exit_on_patterns)
        exit_rules_list = self.calc_entry_rules(box_size, move_count, exit_on_patterns)

        # Median based trailing stop
        trailing_stop = px.rolling(period_median).median().shift(1)

        # Enry/exit rules
        entry_rule = pd.Series(rules_list[rules_index])

        if direction == 1 and exit_on_patterns == False:
            exit_rule = (CrossDown(px, trailing_stop))  # Cross down for longs
            #exit_rule = pd.Series(rules_list[exit_rules_index])
        elif direction == -1 and exit_on_patterns == False:
            exit_rule = (CrossUp(px, trailing_stop))  # Cross up for shorts, Cross down for longs

        if exit_on_patterns == True:
            exit_rule = pd.Series(rules_list[exit_rules_index])



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
