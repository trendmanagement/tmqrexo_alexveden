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


class StrategyIchimokuCloud(StrategyBase):
    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)


    # @numba.jit
    def calc_entry_rules(self, conversion_line_period, base_line_period, leading_spans_lookahead_period,
                         leading_span_b_period, price_df, rules_index):

        # Ichimoku cloud calc

        '''
        Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2))
        The default setting is 9 periods and can be adjusted. On a daily
        chart, this line is the mid point of the 9 day high-low range,
        which is almost two weeks.
        '''
        conversion_line_period = conversion_line_period  # subject of optimization

        conversion_line_high = price_df.rolling(window=conversion_line_period).max()
        conversion_line_low = price_df.rolling(window=conversion_line_period).min()

        conversion_line = (conversion_line_high + conversion_line_low) / 2

        '''
        Kijun-sen (Base Line): (26-period high + 26-period low)/2))
        The default setting is 26 periods and can be adjusted. On a daily
        chart, this line is the mid point of the 26 day high-low range,
        which is almost one month).
        '''
        base_line_period = base_line_period  # subject of optimization

        base_line_high = price_df.rolling(window=base_line_period).max()
        base_line_low = price_df.rolling(window=base_line_period).min()

        base_line = (base_line_high + base_line_low) / 2

        '''
        Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
        This is the midpoint between the Conversion Line and the Base Line.
        The Leading Span A forms one of the two Cloud boundaries. It is
        referred to as "Leading" because it is plotted 26 periods in the future
        and forms the faster Cloud boundary.
        '''
        leading_spans_lookahead_period = leading_spans_lookahead_period  # subject of optimization
        leading_span_a = ((conversion_line + base_line) / 2).shift(leading_spans_lookahead_period)

        # straightforward time shifting to 'leading_spans_lookahead_period' number of days
        # might be slower than .shift method
        # leading_span_a.index = leading_span_a.index + pd.DateOffset(days=leading_spans_lookahead_period)

        '''
        Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
        On the daily chart, this line is the mid point of the 52 day high-low range,
        which is a little less than 3 months. The default calculation setting is
        52 periods, but can be adjusted. This value is plotted 26 periods in the future
        and forms the slower Cloud boundary.
        '''
        leading_span_b_period = leading_span_b_period  # subject of optimization
        leading_span_b = ((price_df.rolling(window=leading_span_b_period).max() + price_df.rolling(
            window=leading_span_b_period).min()) / 2).shift(leading_spans_lookahead_period)

        # straightforward time shifting to 'leading_spans_lookahead_period' number of days
        # might be slower than .shift method
        # leading_span_b.index = leading_span_b.index + pd.DateOffset(days=leading_spans_lookahead_period)

        '''
        Chikou Span (Lagging Span): Close plotted 26 days in the past
        The default setting is 26 periods, but can be adjusted.
        '''
        lagging_span_periods = 26  # subject of optimization
        lagging_span = price_df.shift(-lagging_span_periods)

        #
        # Rules calculation
        #

        # Cloud top and bottom series are defined using leading span A and B
        cloud_top = leading_span_a.rolling(1).max()
        cloud_bottom = leading_span_a.rolling(1).min()

        # 1) cloud color red
        # 2) cloud color green
        if rules_index == 0:
            return leading_span_a > leading_span_b

        elif rules_index == 1:
            return leading_span_a < leading_span_b

        # 3) price is above cloud top
        # 4) price is above cloud bottom

        # Style? rule_.... ?
        elif rules_index == 2:
            return price_df > cloud_top

        elif rules_index == 3:
            return price_df > cloud_bottom

        # 5) price is below cloud top
        # 6) price is below cloud bottom
        elif rules_index == 4:
            return price_df < cloud_top

        elif rules_index == 5:
            return price_df < cloud_bottom

        # 7) conversion and base line crossings
        elif rules_index == 6:
            return CrossUp(conversion_line, base_line)

        elif rules_index == 7:
            return CrossDown(conversion_line, base_line)

        # 8) price and base line crossings
        elif rules_index == 8:
            return CrossUp(price_df, base_line)

        elif rules_index == 9:
            return CrossDown(price_df, base_line)

        # 9) price and conversion line crossings
        elif rules_index == 10:
            return CrossUp(price_df, conversion_line)

        elif rules_index == 11:
            return CrossDown(price_df, conversion_line)

        # 10) is price IN the cloud
        elif rules_index == 12:
            return (price_df < cloud_top) & (price_df > cloud_bottom)

        # 11) spans crossings
        elif rules_index == 13:
            return CrossUp(leading_span_a, leading_span_b)

        elif rules_index == 14:
            return CrossDown(leading_span_a, leading_span_b)

        else:
            raise ValueError('Rules index parameter must be in range of 0-14')

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
            direction, conversion_line_period, base_line_period, leading_spans_lookahead_period, leading_span_b_period, rules_index, period_median = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, conversion_line_period, base_line_period, leading_spans_lookahead_period, leading_span_b_period, rules_index, period_median = params

        # Defining EXO price
        px = self.data.exo

        # Median based trailing stop
        trailing_stop = px.rolling(period_median).median().shift(1)

        # Enry/exit rules
        entry_rule = self.calc_entry_rules(conversion_line_period, base_line_period,
                                           leading_spans_lookahead_period, leading_span_b_period, px, rules_index)

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
