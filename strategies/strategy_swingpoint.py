#!/usr/bin/python

import sys,os
sys.path.append('..')
from backtester import matlab, backtester
from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam
from backtester.common_algos import swingpoints
import pandas as pd
import numpy as np
import scipy



class StrategySwingPoint(StrategyBase):
    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

        # Define system's name
        self.name = 'SwingPoint'

        self.check_context()

        # Define optimized params
        self.opts = strategy_context['strategy']['opt_params']

    def check_context(self):
        #
        # Do strategy specific checks
        #
        pass




    def calc_entry_rules(self, sp_df):

        # Both are EXO close price
        testHPice = testLPrice = sp_df.price
        nDays = len(sp_df)
        longSignalPrice = sp_df['sphLevel'].values
        shortSignalPrice = sp_df['splLevel'].values
        sphVolume = sp_df['sphVolume'].values
        splVolume = sp_df['splVolume'].values
        volumeSeries = sp_df['volumeSeries'].values

        # Filling results with zeros
        bullish_breakout_confirmed = np.zeros(nDays, dtype=np.int8)
        bearish_breakout_confirmed = np.zeros(nDays, dtype=np.int8)
        bullish_failure_confirmed = np.zeros(nDays, dtype=np.int8)
        bearish_failure_confirmed = np.zeros(nDays, dtype=np.int8)

        #
        # Failures flags and settings
        #
        confirmationThreshold = 10   # How many bars to confirm failure
        longPenetrationCount = 0
        shortPenetrationCount = 0
        longFailureFlag = False
        shortFailureFlag = False
        failureLongLine = 0.0
        failureShortLine = 0.0


        for dd in range(1, nDays):
            #
            # Bullish breakout confirmed rule
            #
            if testHPice[dd] > longSignalPrice[dd-1] and testHPice[dd-1] < longSignalPrice[dd-1]: #  Check the cross of sphLevel
                bullish_breakout_confirmed[dd] = 1
                # Failures flag set
                longFailureFlag = True
                longPenetrationCount = 0
                failureLongLine = testHPice[dd-1]

            #
            # Bearish breakout confirmed rule
            #
            if testLPrice[dd] < shortSignalPrice[dd-1] and testLPrice[dd-1] > shortSignalPrice[dd-1]: #   Check the cross of splLevel
                bearish_breakout_confirmed[dd] = 1
                # Failures flag set
                shortFailureFlag = True
                shortPenetrationCount = 0
                failureShortLine = testLPrice[dd-1]


            #
            # Bullish failure test
            #
            if longFailureFlag:
                # If crossing previous failure line
                if testHPice[dd] < failureLongLine and testHPice[dd-1] > failureLongLine \
                    and longPenetrationCount <= confirmationThreshold:
                        bullish_failure_confirmed[dd] = 1
                else:
                    longPenetrationCount += 1
                    if longPenetrationCount > confirmationThreshold:
                        longFailureFlag = False
            #
            # Bearish failure test
            #
            if shortFailureFlag:
                # If crossing previous failure line
                if testLPrice[dd] > failureShortLine and testLPrice[dd-1] < failureShortLine \
                    and shortPenetrationCount <= confirmationThreshold:
                        bearish_failure_confirmed[dd] = 1
                else:
                    shortPenetrationCount += 1
                    if shortPenetrationCount > confirmationThreshold:
                        shortFailureFlag = False


        return bearish_breakout_confirmed, bearish_failure_confirmed, bullish_breakout_confirmed, bullish_failure_confirmed




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
            direction, sphTreshold_value, splTreshold_value, rules_index, period_median = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            direction, sphTreshold_value, splTreshold_value, rules_index, period_median = params

        # Defining EXO price
        px = self.data.exo

        #
        #
        # Swing poins rules calculation
        #
        #
        '''
        testHPrice = optStr.entrySignalingSeries(CLOSE,dd);   Note OPEN=1, HIGH=2, LOW=3, CLOSE=4
        testLPrice = optStr.entrySignalingSeries(CLOSE,dd);

        longSignalPrice      = sphLevel(dd-1);    % swing point high value on the previous day
        shortSignalPrice     = splLevel(dd-1);    % swing point low value on the previous day

        optStr.sphVolume     = the volume on the last swing-point-high day
        optStr.splVolume     = the volume on the last swing-point-low  day
        '''

        # Setting Swing point DF
        sp_df = swingpoints(sphTreshold_value, splTreshold_value, self.data)

        rules_list = self.calc_entry_rules(sp_df)

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
            calc_info = {'trailing_stop': trailing_stop, 'sp_df': sp_df}

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
