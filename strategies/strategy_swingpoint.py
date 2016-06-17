#!/usr/bin/python

import sys,os
sys.path.append('..')
from backtester import matlab, backtester
from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam
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

    def swingpoints(self, sphThreshold, splThreshold, data):

        '''
        !Required for mat file loading! from scipy.io import loadmat, savemat

        sphTreshold - int number of days from breakout
        splTreshold - int number of days from breakout
        data - exo data (including exo price and volume)

        returns -> df with sphLevel/volume and splLevel/volume pd series with exo prices index.
                    Plus VolumeSeries and price with exo prices index
        '''

        signalArray = data.exo.values
        volumeArray = data.volume.values

        OPEN  = 0
        HIGH  = 1
        LOW   = 2
        CLOSE = 3

        if len(signalArray) == 1:
            OPEN = HIGH = LOW = CLOSE = 0

        currentHigh = -np.inf  # intmin('int32');
        currentLow = np.inf  # intmax('int32');

        currentHVol = 0
        currentLVol = 0
        sphDays = 0
        splDays = 0
        sphStart = 1
        splStart = 1
        sphMaxDay = 0
        splMinDay = 0
        prevHigh = signalArray[0]
        prevLow = signalArray[0]
        prevHVol = volumeArray[0]
        prevLVol = volumeArray[0]

        nDays = len(signalArray)

        sphIndicator = np.zeros(nDays)
        splIndicator = np.zeros(nDays)

        sphLevel = np.zeros(nDays)
        splLevel = np.zeros(nDays)

        sphVolume = np.zeros(nDays)
        splVolume = np.zeros(nDays)

        for dday in range(nDays):

            if signalArray[dday] > currentHigh:
                currentHigh = signalArray[dday]
                currentHVol = volumeArray[dday]
                sphMaxDay = dday
                sphDays = 0
            else:
                sphDays = sphDays + 1

            if signalArray[dday] < currentLow:
                currentLow = signalArray[dday]
                currentLVol = volumeArray[dday]
                splMinDay = dday
                splDays = 0
            else:
                splDays = splDays + 1

            if sphDays > sphThreshold:
                sphLevel[dday] = currentHigh
                sphIndicator[dday] = 1
                sphVolume[dday] = currentHVol

                for dd in range(sphStart, dday):  # ?? or dday-1
                    sphLevel[dd] = prevHigh
                    sphVolume[dd] = prevHVol

                prevHigh = currentHigh
                prevHVol = currentHVol
                sphStart = dday
                sphDays = 0
                currentHigh = -np.inf  # intmin('int32');

            elif dday > 1:
                sphVolume[dday] = sphVolume[dday - 1]
            elif dday == 1:
                sphVolume[dday] = volumeArray[dday]

            if splDays > splThreshold:
                splLevel[dday] = currentLow
                splIndicator[dday] = 1
                splVolume[dday] = currentLVol

                for dd in range(splStart, dday):  # ??? or dday-1
                    splLevel[dd] = prevLow
                    splVolume[dd] = prevLVol

                prevLow = currentLow
                prevLVol = currentLVol
                splStart = dday
                splDays = 0
                currentLow = np.inf  # intmax('int32');
            elif dday > 1:
                splVolume[dday] = splVolume[dday - 1]
            elif dday == 1:
                splVolume[dday] = volumeArray[dday]

            # fill to the end
            for dd in range(sphStart, nDays):
                sphLevel[dd] = prevHigh
                sphVolume[dd] = prevHVol

            for dd in range(splStart, nDays):
                splLevel[dd] = prevLow
                splVolume[dd] = prevLVol

        return pd.DataFrame(
            {
                 'sphIndicator': pd.Series(sphIndicator, index=data.exo.index),
                 'splIndicator': pd.Series(splIndicator, index=data.exo.index),
                 'sphLevel': pd.Series(sphLevel, index=data.exo.index),
                 'splLevel': pd.Series(splLevel, index=data.exo.index),
                 'sphVolume': pd.Series(sphVolume, index=data.exo.index),
                 'splVolume': pd.Series(splVolume, index=data.exo.index),
                 'volumeSeries': pd.Series(volumeArray, index=data.exo.index),
                 'price':  pd.Series(data.exo, index=data.exo.index)
            },
            index=data.exo.index)


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
        sp_df = self.swingpoints(sphTreshold_value, splTreshold_value, self.data)

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
