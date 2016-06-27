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

        # Define system's name
        self.name = 'IchimokuCloud'

        self.check_context()

        # Define optimized params
        self.opts = strategy_context['strategy']['opt_params']

    def check_context(self):
        #
        # Do strategy specific checks
        #
        pass

    def calc_entry_rules(self, conversion_line_period, base_line_period, leading_spans_lookahead_period,
                         leading_span_b_period,
                         price_df):

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
        leading_span_a = ((conversion_line + base_line) / 2)

        # straightforward time shifting to 'leading_spans_lookahead_period' number of days
        leading_span_a.index = leading_span_a.index + pd.DateOffset(days=leading_spans_lookahead_period)

        '''
        Senkou Span B (Leading Span B): (52-period high + 52-period low)/2)) 

        On the daily chart, this line is the mid point of the 52 day high-low range, 
        which is a little less than 3 months. The default calculation setting is 
        52 periods, but can be adjusted. This value is plotted 26 periods in the future 
        and forms the slower Cloud boundary.
        '''
        leading_span_b_period = leading_span_b_period  # subject of optimization
        leading_span_b = ((price_df.rolling(window=leading_span_b_period).max() + price_df.rolling(
            window=leading_span_b_period).min()) / 2)

        # straightforward time shifting to 'leading_spans_lookahead_period' number of days
        leading_span_b.index = leading_span_b.index + pd.DateOffset(days=leading_spans_lookahead_period)

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
        cloud_top = leading_span_a.combine(leading_span_b, max, 0)
        cloud_bottom = leading_span_a.combine(leading_span_b, min, 0)

        # 1) cloud color red
        # 2) cloud color green
        cloud_color_green = leading_span_a > leading_span_b
        cloud_color_red = leading_span_a < leading_span_b

        # 3) price is above cloud top
        # 4) price is above cloud bottom

        # Style? rule_.... ?
        price_above_cloud_top = price_df > cloud_top
        price_above_cloud_bottom = price_df > cloud_bottom

        # 5) price is below cloud top
        # 6) price is below cloud bottom
        price_below_cloud_top = price_df < cloud_top
        price_below_cloud_bottom = price_df < cloud_bottom

        # 7) conversion and base line crossings
        conv_crossup_base_line = CrossUp(conversion_line, base_line)
        conv_crossdown_base_line = CrossDown(conversion_line, base_line)

        # 8) price and base line crossings
        price_crossup_base_line = CrossUp(price_df, base_line)
        price_crossdown_base_line = CrossDown(price_df, base_line)

        # 9) price and conversion line crossings
        price_crossup_conv_line = CrossUp(price_df, conversion_line)
        price_crossdown_conv_line = CrossDown(price_df, conversion_line)

        # 10) is price IN the cloud
        price_in_cloud = (price_df < cloud_top) & (price_df > cloud_bottom)

        # 11) spans crossings
        spans_crossup = CrossUp(leading_span_a, leading_span_b)
        spans_crossdown = CrossDown(leading_span_a, leading_span_b)

        return cloud_color_green, cloud_color_red, price_above_cloud_top, price_above_cloud_bottom, price_below_cloud_top, price_below_cloud_bottom, price_crossup_base_line, price_crossdown_base_line, price_crossup_conv_line, price_crossdown_base_line, price_crossup_conv_line, price_crossdown_conv_line, price_in_cloud, conv_crossup_base_line, conv_crossdown_base_line, spans_crossup, spans_crossdown

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

        rules_list = self.calc_entry_rules(conversion_line_period, base_line_period,
                                           leading_spans_lookahead_period, leading_span_b_period, px)

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
