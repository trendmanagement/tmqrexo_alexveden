from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam

import pandas as pd
import numpy as np
import scipy


class StrategyPointAndFigurePatterns(StrategyBase):
    # Define system's name
       
    name = 'PointAndFigurePatterns'

    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)


    def calc_entry_rules(self, box_size, reversal_multiplier, column_consec_move_count, window_percent, rules_index):

        df = pd.DataFrame()

        px = self.data

        df['close'] = self.data.exo

        box_size = box_size

        box_start = 0
        box_start_idx = None

        box_end = 0
        box_quantity = 0

        temp_l = []

        column_flag = None

        reversal_multiplier = reversal_multiplier
        reversal_value = box_size * reversal_multiplier

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
                        if price_move < 0 and price_move <= -reversal_value:
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
                        if price_move > 0 and price_move >= reversal_value:
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
        if rules_index == 0:
            pnf_df['new_x_col'] = (pnf_df.type == 'x') & (pnf_df.type.shift(1) == 'o')
            signals_df = px.join(pnf_df.set_index('date')[['new_x_col']])
            signals_df = signals_df.fillna(False).groupby(signals_df.index).any()

            return signals_df.new_x_col == True

        if rules_index == 1:
            pnf_df['new_o_col'] = (pnf_df.type == 'o') & (pnf_df.type.shift(1) == 'x')
            signals_df = px.join(pnf_df.set_index('date')[['new_o_col']])
            signals_df = signals_df.fillna(False).groupby(signals_df.index).any()

            return signals_df.new_o_col == True

        if rules_index == 2:
            pnf_df['tripple_top'] = pnf_last_column_value_df[pnf_last_column_value_df.type == 'x'].close == \
                                    pnf_last_column_value_df[pnf_last_column_value_df.type == 'x'].close.shift(1)

            pnf_df['tripple_top'] = pnf_df['tripple_top'].fillna(False)

            pnf_df['tripple_top_price_level'] = pnf_df[pnf_df.tripple_top == True].groupby(
                pnf_df[pnf_df.tripple_top == True].index).last().close
            pnf_df['tripple_top_price_level'] = pnf_df['tripple_top_price_level'].ffill()

            pnf_df['tripple_top_breakout'] = (
                (pnf_df.close == pnf_df.tripple_top_price_level) & (
                    pnf_df.close.shift(1) < pnf_df.tripple_top_price_level)
                & (pnf_df.tripple_top == False))

            tripple_top_breakout_dup = pnf_df[pnf_df.tripple_top_breakout == True][
                'tripple_top_price_level'].duplicated()

            pnf_df.loc[tripple_top_breakout_dup[tripple_top_breakout_dup == True].index, 'tripple_top_breakout'] = \
                pnf_df.tripple_top_breakout.ix[
                    tripple_top_breakout_dup[tripple_top_breakout_dup == True].index].replace(True, False)

            signals_df = px.join(pnf_df.set_index('date')[['tripple_top_breakout']])
            signals_df = signals_df.fillna(False).groupby(signals_df.index).any()

            return signals_df.tripple_top_breakout == True

        if rules_index == 3:
            pnf_df['tripple_bot'] = pnf_last_column_value_df[pnf_last_column_value_df.type == 'o'].close == \
                                    pnf_last_column_value_df[pnf_last_column_value_df.type == 'o'].close.shift(1)

            pnf_df['tripple_bot'] = pnf_df['tripple_bot'].fillna(False)

            pnf_df['tripple_bot_price_level'] = pnf_df[pnf_df.tripple_bot == True].groupby(
                pnf_df[pnf_df.tripple_bot == True].index).last().close
            pnf_df['tripple_bot_price_level'] = pnf_df['tripple_bot_price_level'].ffill()

            pnf_df['tripple_bot_breakout'] = (
                (pnf_df.close == pnf_df.tripple_bot_price_level) & (
                    pnf_df.close.shift(1) > pnf_df.tripple_bot_price_level)
                & (pnf_df.tripple_bot == False))

            tripple_bot_breakout_dup = pnf_df[pnf_df.tripple_bot_breakout == True][
                'tripple_bot_price_level'].duplicated()

            pnf_df.loc[tripple_bot_breakout_dup[tripple_bot_breakout_dup == True].index, 'tripple_bot_breakout'] = \
                pnf_df.tripple_bot_breakout.ix[
                    tripple_bot_breakout_dup[tripple_bot_breakout_dup == True].index].replace(True, False)

            signals_df = px.join(pnf_df.set_index('date')[['tripple_bot_breakout']])
            signals_df = signals_df.fillna(False).groupby(signals_df.index).any()

            return signals_df.tripple_bot_breakout == True

        if rules_index == 4:

            up_move_count = [0]
            up_move_counter = 0

            x_col_upmove = pnf_last_column_value_df[pnf_last_column_value_df.type == 'x'].close > \
                           pnf_last_column_value_df[pnf_last_column_value_df.type == 'x'].close.shift(1)

            for i in x_col_upmove.index.unique():
                if x_col_upmove[i] == True and x_col_upmove.shift(1)[i] == False:
                    up_move_counter = 1
                    up_move_count.append(up_move_counter)

                elif x_col_upmove[i] == True and x_col_upmove.shift(1)[i] == True:
                    up_move_counter += 1
                    up_move_count.append(up_move_counter)

                elif x_col_upmove[i] == False and x_col_upmove.shift(1)[i] == True:
                    up_move_counter = 0
                    up_move_count.append(up_move_counter)

                elif x_col_upmove[i] == False and x_col_upmove.shift(1)[i] == False:
                    up_move_counter = 0
                    up_move_count.append(up_move_counter)

            pnf_df['x_col_upmove_count'] = pd.Series(up_move_count, index=x_col_upmove.index)

            signals_df = px.join(pnf_df.set_index('date')[['x_col_upmove_count']])
            signals_df = signals_df.ffill().groupby(signals_df.index).last()

            return signals_df.x_col_upmove_count == column_consec_move_count

        if rules_index == 5:
            down_move_count = [0]
            down_move_counter = 0

            x_col_downmove = pnf_last_column_value_df[pnf_last_column_value_df.type == 'x'].close < \
                             pnf_last_column_value_df[pnf_last_column_value_df.type == 'x'].close.shift(1)

            for i in x_col_downmove.index.unique():
                if x_col_downmove[i] == True and x_col_downmove.shift(1)[i] == False:
                    down_move_counter = 1
                    down_move_count.append(down_move_counter)

                elif x_col_downmove[i] == True and x_col_downmove.shift(1)[i] == True:
                    down_move_counter += 1
                    down_move_count.append(down_move_counter)

                elif x_col_downmove[i] == False and x_col_downmove.shift(1)[i] == True:
                    down_move_counter = 0
                    down_move_count.append(down_move_counter)

                elif x_col_downmove[i] == False and x_col_downmove.shift(1)[i] == False:
                    down_move_counter = 0
                    down_move_count.append(down_move_counter)

            pnf_df['x_col_downmove_count'] = pd.Series(down_move_count, index=x_col_downmove.index)
            signals_df = px.join(pnf_df.set_index('date')[['x_col_downmove_count']])
            signals_df = signals_df.ffill().groupby(signals_df.index).last()

            return signals_df.x_col_downmove_count == column_consec_move_count

        if rules_index == 6:
            same_move_count = [0]
            same_move_counter = 0

            x_col_samemove = pnf_last_column_value_df[pnf_last_column_value_df.type == 'x'].close == \
                             pnf_last_column_value_df[pnf_last_column_value_df.type == 'x'].close.shift(1)

            for i in x_col_samemove.index.unique():
                if x_col_samemove[i] == True and x_col_samemove.shift(1)[i] == False:
                    same_move_counter = 1
                    same_move_count.append(same_move_counter)

                elif x_col_samemove[i] == True and x_col_samemove.shift(1)[i] == True:
                    same_move_counter += 1
                    same_move_count.append(same_move_counter)

                elif x_col_samemove[i] == False and x_col_samemove.shift(1)[i] == True:
                    same_move_counter = 0
                    same_move_count.append(same_move_counter)

                elif x_col_samemove[i] == False and x_col_samemove.shift(1)[i] == False:
                    same_move_counter = 0
                    same_move_count.append(same_move_counter)

            pnf_df['x_col_samemove_count'] = pd.Series(same_move_count, index=x_col_samemove.index)
            signals_df = px.join(pnf_df.set_index('date')[['x_col_samemove_count']])
            signals_df = signals_df.ffill().groupby(signals_df.index).last()

            return signals_df.x_col_samemove_count == column_consec_move_count

        if rules_index == 7:
            up_move_count = [0]
            up_move_counter = 0

            o_col_upmove = pnf_last_column_value_df[pnf_last_column_value_df.type == 'o'].close > \
                           pnf_last_column_value_df[pnf_last_column_value_df.type == 'o'].close.shift(1)

            for i in o_col_upmove.index.unique():
                if o_col_upmove[i] == True and o_col_upmove.shift(1)[i] == False:
                    up_move_counter = 1
                    up_move_count.append(up_move_counter)

                elif o_col_upmove[i] == True and o_col_upmove.shift(1)[i] == True:
                    up_move_counter += 1
                    up_move_count.append(up_move_counter)

                elif o_col_upmove[i] == False and o_col_upmove.shift(1)[i] == True:
                    up_move_counter = 0
                    up_move_count.append(up_move_counter)

                elif o_col_upmove[i] == False and o_col_upmove.shift(1)[i] == False:
                    up_move_counter = 0
                    up_move_count.append(up_move_counter)

            pnf_df['o_col_upmove_count'] = pd.Series(up_move_count, index=o_col_upmove.index)

            signals_df = px.join(pnf_df.set_index('date')[['o_col_upmove_count']])
            signals_df = signals_df.ffill().groupby(signals_df.index).last()

            return signals_df.o_col_upmove_count == column_consec_move_count

        if rules_index == 8:

            down_move_count = [0]
            down_move_counter = 0

            o_col_downmove = pnf_last_column_value_df[pnf_last_column_value_df.type == 'o'].close < \
                             pnf_last_column_value_df[pnf_last_column_value_df.type == 'o'].close.shift(1)

            for i in o_col_downmove.index.unique():
                if o_col_downmove[i] == True and o_col_downmove.shift(1)[i] == False:
                    down_move_counter = 1
                    down_move_count.append(down_move_counter)

                elif o_col_downmove[i] == True and o_col_downmove.shift(1)[i] == True:
                    down_move_counter += 1
                    down_move_count.append(down_move_counter)

                elif o_col_downmove[i] == False and o_col_downmove.shift(1)[i] == True:
                    down_move_counter = 0
                    down_move_count.append(down_move_counter)

                elif o_col_downmove[i] == False and o_col_downmove.shift(1)[i] == False:
                    down_move_counter = 0
                    down_move_count.append(down_move_counter)

            pnf_df['o_col_downmove_count'] = pd.Series(down_move_count, index=o_col_downmove.index)

            signals_df = px.join(pnf_df.set_index('date')[['o_col_downmove_count']])
            signals_df = signals_df.ffill().groupby(signals_df.index).last()

            return signals_df.o_col_downmove_count == column_consec_move_count

        if rules_index == 9:
            same_move_count = [0]
            same_move_counter = 0

            o_col_samemove = pnf_last_column_value_df[pnf_last_column_value_df.type == 'o'].close == \
                             pnf_last_column_value_df[pnf_last_column_value_df.type == 'o'].close.shift(1)

            for i in o_col_samemove.index.unique():
                if o_col_samemove[i] == True and o_col_samemove.shift(1)[i] == False:
                    same_move_counter = 1
                    same_move_count.append(same_move_counter)

                elif o_col_samemove[i] == True and o_col_samemove.shift(1)[i] == True:
                    same_move_counter += 1
                    same_move_count.append(same_move_counter)

                elif o_col_samemove[i] == False and o_col_samemove.shift(1)[i] == True:
                    same_move_counter = 0
                    same_move_count.append(same_move_counter)

                elif o_col_samemove[i] == False and o_col_samemove.shift(1)[i] == False:
                    same_move_counter = 0
                    same_move_count.append(same_move_counter)

            pnf_df['o_col_samemove_count'] = pd.Series(same_move_count, index=o_col_samemove.index)

            signals_df = px.join(pnf_df.set_index('date')[['o_col_samemove_count']])
            signals_df = signals_df.ffill().groupby(signals_df.index).last()

            return signals_df.o_col_samemove_count == column_consec_move_count

        if rules_index == 10:
            for i in pnf_df.index.unique():
                if pnf_df.close.ix[i].size > 1.0:
                    pnf_df.loc[i, 'box_count'] = pnf_df.close.ix[i].count()

                else:
                    pnf_df.loc[i, 'box_count'] = 1.0

            bull_fail = ((pnf_df.box_count == reversal_multiplier) & (pnf_df.type == 'x')).groupby(
                ((pnf_df.box_count == reversal_multiplier)
                 & (pnf_df.type == 'x')).index).last()

            pnf_first_column_value_df['bullish_failure'] = (bull_fail.shift(1) == True).groupby(
                (bull_fail.shift(1) == True).index).first()

            signals_df = px.join(pnf_first_column_value_df.set_index('date')[
                                     ['bullish_failure']])

            return signals_df.bullish_failure == True

        if rules_index == 11:
            for i in pnf_df.index.unique():
                if pnf_df.close.ix[i].size > 1.0:
                    pnf_df.loc[i, 'box_count'] = pnf_df.close.ix[i].count()

                else:
                    pnf_df.loc[i, 'box_count'] = 1.0

            bear_fail = ((pnf_df.box_count == reversal_multiplier) & (pnf_df.type == 'o')).groupby(
                ((pnf_df.box_count == reversal_multiplier)
                 & (pnf_df.type == 'o')).index).last()

            pnf_first_column_value_df['bearish_failure'] = (bear_fail.shift(1) == True).groupby(
                (bear_fail.shift(1) == True).index).first()

            signals_df = px.join(pnf_first_column_value_df.set_index('date')[
                                     ['bearish_failure']])
            signals_df = signals_df.fillna(False).groupby(signals_df.index).any()

            return signals_df.bearish_failure == True

        if rules_index == 12:
            pnf_first_column_value_df['local_high'] = (pnf_last_column_value_df.close == pnf_last_column_value_df.close.rolling(len(
                                                                  pnf_last_column_value_df.close) * window_percent).max()).shift(1) == True

            signals_df = px.join(pnf_first_column_value_df.set_index('date')[
                                     ['local_high']])
            signals_df = signals_df.fillna(False).groupby(signals_df.index).any()

            return signals_df.local_high == True

        if rules_index == 13:
            pnf_first_column_value_df['local_low'] = (pnf_last_column_value_df.close == pnf_last_column_value_df.close.rolling(
                                                             len(pnf_last_column_value_df.close) * window_percent).min()).shift(1) == True

            signals_df = px.join(pnf_first_column_value_df.set_index('date')[
                                     ['local_low']])
            signals_df = signals_df.fillna(False).groupby(signals_df.index).any()

            return signals_df.local_low == True

        if rules_index > 13:
            raise ValueError('Rules index parameter must be in range of 0-13')

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
            direction, box_size, reversal_multiplier, window_percent, column_consec_move_count, rules_index, period_median = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, box_size, reversal_multiplier, window_percent, column_consec_move_count, rules_index, period_median = params

        # Defining EXO price
        px = self.data.exo

        # Median based trailing stop
        trailing_stop = px.rolling(period_median).median().shift(1)

        # Enry/exit rules
        entry_rule = self.calc_entry_rules(box_size, reversal_multiplier, window_percent, column_consec_move_count,
                                           rules_index)

        if direction == 1:
            exit_rule = (CrossDown(px, trailing_stop))  # Cross down for longs
        elif direction == -1:
            exit_rule = (CrossUp(px, trailing_stop))  # Cross up for shorts, Cross down for longs



            # exit_rule = pd.Series(rules_list[exit_rules_index])
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