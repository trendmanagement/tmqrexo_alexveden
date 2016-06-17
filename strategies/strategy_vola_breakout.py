#!/usr/bin/python

import sys,os
sys.path.append('..')
from backtester import matlab, backtester
from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam
import pandas as pd
import numpy as np
import scipy



class StrategyVolaBreakoutBands(StrategyBase):
    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

        # Define system's name
        self.name = 'VolatilityBreakout'

        self.check_context()

        # This is a short strategy
        self.direction = strategy_context['strategy']['direction']

        # Define optimized params
        self.opts = strategy_context['strategy']['opt_params']

    def check_context(self):
        #
        # Do strategy specific checks
        #
        pass


    @property
    def positionsize(self):
        """
        Returns volatility adjuster positions size for strategy
        :return:
        """

        # Defining EXO price
        px = self.data.exo
        # Test !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return pd.Series(1.0, index=px.index)


    def calculate(self, params=None, save_info=False):

        # Unpacking params values
        direction, period, down_factor, up_factor = params

        # Defining EXO price
        px = self.data.exo

        #
        # Indicator calculation
        #
        #

        vola = px.diff(periods=period).abs().rolling(60).median()

        swing_point = pd.Series(np.nan, index=px.index)
        swing_point_regime = pd.Series(0, index=px.index)

        # Swing point bullish regime
        swing_switch = 1

        # Swing point start index
        sw_i = -1

        # Min/Max prices for swings
        sw_h_max = px[0]
        sw_l_min = px[0]

        for i in range(len(px)):
            if i == 0:
                continue
            if np.isnan(px[i]):
                continue
            if np.isnan(vola.values[i]):
                continue
            elif sw_i == -1 and vola.values[i] > 0:
                sw_h_max = sw_l_min = px[i]
                sw_i = i

            if swing_switch == 1:
                #
                #  We have a bullish swing
                #
                sw_h_max = max(sw_h_max, px[i])

                # Check for reversion
                if px[i] <= sw_h_max - vola[sw_i] * down_factor:
                    # Reverse swing
                    swing_switch = -1
                    sw_l_min = px.values[i]
                    sw_h_max = px.values[i]
                    swing_point.values[i] = sw_l_min + vola[sw_i] * up_factor

                    sw_i = i
                else:
                    swing_point.values[i] = sw_h_max - vola[sw_i] * down_factor


            else:
                #
                #  We have a bearish swing
                #
                sw_l_min = min(sw_l_min, px.values[i])

                # Check for reversion
                if px.values[i] >= sw_l_min + vola[sw_i] * up_factor:
                    # Reverse swing
                    swing_switch = 1
                    sw_l_min = px.values[i]
                    sw_h_max = px.values[i]
                    sw_i = i
                    swing_point.values[i] = sw_h_max - vola[sw_i] * down_factor
                else:
                    swing_point.values[i] = sw_l_min + vola[sw_i] * up_factor

            swing_point_regime.values[i] = swing_switch
        
        # Enry/exit rules
        if direction == 1:
            entry_rule = swing_point_regime == 1
            exit_rule = swing_point_regime == -1
        else:
            entry_rule = swing_point_regime == -1
            exit_rule = swing_point_regime == 1

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        #
        # Calculation info
        #
        calc_info = None
        if save_info:
            calc_info = {'swing_point': swing_point, 'swing_point_regime': swing_point_regime}

        return swarm_member_name, entry_rule, exit_rule, calc_info

if __name__ == "__main__":
    #
    #   Run this code only from direct shell execution
    #
    #strategy = StrategyMACrossTrail()
    #equity, stats = strategy.calculate()

    # Do some work
    data, info = matlab.loaddata('../mat/strategy_270225.mat')
    data.plot()