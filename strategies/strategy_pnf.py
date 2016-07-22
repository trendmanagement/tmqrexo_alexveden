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


class StrategyPointAndFigurePatterns(StrategyBase):
    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

        # Define system's name
        self.name = 'PointAndFigurePatterns'

        self.check_context()

        # Define optimized params
        self.opts = strategy_context['strategy']['opt_params']

    def check_context(self):
        #
        # Do strategy specific checks
        #
        pass

    def calc_entry_rules(self, box_size, reversal_value):


        df = pd.DataFrame()

        px = self.data

        if ((np.abs(px.min()) + np.abs(px.max())) / 2).values[0] >= 10000:
            df['close'] = self.data.exo / 100

        elif ((np.abs(px.min()) + np.abs(px.max())) / 2).values[0] >= 1000:
            df['close'] = self.data.exo / 10

        else:
            df['close'] = self.data.exo

        box_size = box_size

        box_start = 0
        box_start_idx = None

        box_end = 0
        box_quantity = 0

        temp_l = []

        column_flag = None

        reversal_value = box_size * reversal_value

        reversal_flag = False

        column_index = 0

        # Simple point and figure algorihtm

        for i in range(len(df)):
            if box_start == 0:
                box_start = df.close[i]

            else:
                box_start = box_start
                price_move = df.close[i] - box_start

                # First of all we need to set box size.
                # Then calculate price movement.
                # If price movement is more or equal than box size - x-o boxes will be added

                if np.abs(price_move) >= box_size:

                    # After we calculate box_quantity(price move divided by box size)
                    # This number defines how much pnf boxes will be registred
                    box_quantity = np.int32(np.floor(np.abs(price_move / box_size)))
                    box_date = df.close.index[i]

                    if column_flag == 'x' and reversal_flag == False:

                        # Reversal check
                        if price_move < 0 and box_quantity >= reversal_value:
                            reversal_flag = True
                            box_start = temp_l[-1]['open']


                        elif price_move > 0:
                            reversal_flag = False

                            for b in range(int(box_quantity)):
                                d = {'date': box_date, 'open': box_end, 'close': box_end + box_size,
                                     'type': column_flag, 'column_index': column_index}

                                box_end = d['close']
                                temp_l.append(d)

                    if column_flag == 'o' and reversal_flag == False:

                        # Reversal check
                        if price_move > 0 and box_quantity >= reversal_value:
                            reversal_flag = True
                            box_start = temp_l[-1]['open']


                        elif price_move < 0:
                            reversal_flag = False

                            for b in range(int(box_quantity)):
                                d = {'date': box_date, 'open': box_end, 'close': box_end - box_size,
                                     'type': column_flag, 'column_index': column_index}

                                box_end = d['close']
                                temp_l.append(d)

                    if column_flag == None and reversal_flag == False:

                        # Adding first column

                        if price_move > 0:
                            column_flag = 'x'

                        if price_move < 0:
                            column_flag = 'o'

                        for b in range(int(box_quantity)):
                            if column_flag == 'x':

                                if box_end == 0:
                                    d = {'date': box_date, 'open': box_start, 'close': box_start + box_size,
                                         'type': column_flag,
                                         'column_index': column_index}

                                    box_end = d['close']
                                    temp_l.append(d)

                                else:
                                    d = {'date': box_date, 'open': box_end, 'close': box_end + box_size,
                                         'type': column_flag,
                                         'column_index': column_index}

                                    box_end = d['close']
                                    temp_l.append(d)

                            if column_flag == 'o':

                                if box_end == 0:
                                    d = {'date': box_date, 'open': box_start, 'close': box_start - box_size,
                                         'type': column_flag, 'column_index': column_index}

                                    box_end = d['close']
                                    temp_l.append(d)

                                else:
                                    d = {'date': box_date, 'open': box_end, 'close': box_end - box_size,
                                         'type': column_flag,
                                         'column_index': column_index}

                                    box_end = d['close']
                                    temp_l.append(d)

                    # Handling the reversals
                    if reversal_flag == True:
                        column_index += 1

                        if column_flag == 'x':

                            column_flag = 'o'

                            for b in range(int(box_quantity)):
                                d = {'date': box_date, 'open': box_end, 'close': box_end - box_size,
                                     'type': column_flag, 'column_index': column_index}

                                box_end = d['close']
                                temp_l.append(d)

                        elif column_flag == 'o':

                            column_flag = 'x'

                            for b in range(int(box_quantity)):
                                d = {'date': box_date, 'open': box_end, 'close': box_end + box_size,
                                     'type': column_flag, 'column_index': column_index}

                                box_end = d['close']
                                temp_l.append(d)

                        reversal_flag = False
                try:
                    box_start = temp_l[-1]['close']

                except IndexError:
                    box_start = df.close[i]

        pnf_df = pd.DataFrame(temp_l)
        pnf_df.index = pnf_df.column_index

        pnf_last_column_value_df = pnf_df.groupby(pnf_df.index).last()
        pnf_first_column_value_df = pnf_df.groupby(pnf_df.index).first()

        # New x column

        pnf_prev1_df = pnf_df.shift(1)

        # pnf_prev1_last_column_value_df = pnf_df.shift(1).groupby(pnf_df.index).last()

        pnf_df['new_x_col'] = (pnf_df.type == 'x') & (pnf_df.type.shift(1) == 'o')
        pnf_df['new_o_col'] = (pnf_df.type == 'o') & (pnf_df.type.shift(1) == 'x')

        pnf_df['tripple_top'] = pnf_last_column_value_df[pnf_last_column_value_df.type == 'x'].close == \
                                pnf_last_column_value_df[pnf_last_column_value_df.type == 'x'].close.shift(1)

        pnf_df['tripple_top'] = pnf_df['tripple_top'].fillna(False)

        pnf_df['tripple_top_price_level'] = pnf_df[pnf_df.tripple_top == True].groupby(
            pnf_df[pnf_df.tripple_top == True].index).last().close
        pnf_df['tripple_top_price_level'] = pnf_df['tripple_top_price_level'].ffill()

        pnf_df['tripple_top_breakout'] = (
        (pnf_df.close == pnf_df.tripple_top_price_level) & (pnf_df.close.shift(1) < pnf_df.tripple_top_price_level)
        & (pnf_df.tripple_top == False))

        pnf_df['tripple_bot'] = pnf_last_column_value_df[pnf_last_column_value_df.type == 'o'].close == \
                                pnf_last_column_value_df[pnf_last_column_value_df.type == 'o'].close.shift(1)

        pnf_df['tripple_bot'] = pnf_df['tripple_bot'].fillna(False)

        pnf_df['tripple_bot_price_level'] = pnf_df[pnf_df.tripple_bot == True].groupby(
            pnf_df[pnf_df.tripple_bot == True].index).last().close
        pnf_df['tripple_bot_price_level'] = pnf_df['tripple_bot_price_level'].ffill()

        pnf_df['tripple_bot_breakout'] = (
        (pnf_df.close == pnf_df.tripple_bot_price_level) & (pnf_df.close.shift(1) > pnf_df.tripple_bot_price_level)
        & (pnf_df.tripple_bot == False))

        px.join(pnf_df.set_index('date')[['new_x_col', 'new_o_col', 'tripple_bot_breakout', 'tripple_top_breakout']])


        signals_df = px.join(pnf_df.set_index('date')[['new_x_col', 'new_o_col', 'tripple_bot_breakout', 'tripple_top_breakout']])

        return signals_df.new_x_col == True, signals_df.new_o_col == True, signals_df.tripple_bot_breakout == True, \
               signals_df.tripple_top_breakout == True

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
            direction, box_size, reversal_value, rules_index, period_median = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, box_size, reversal_value, rules_index, period_median = params

        # Defining EXO price
        px = self.data.exo

        rules_list = self.calc_entry_rules(box_size, reversal_value)

        # Median based trailing stop
        trailing_stop = px.rolling(period_median).median().shift(1)

        # Enry/exit rules
        entry_rule = pd.Series(rules_list[rules_index])

        if direction == 1:
            exit_rule = (CrossDown(px, trailing_stop))  # Cross down for longs
            #exit_rule = pd.Series(rules_list[exit_rules_index])
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
