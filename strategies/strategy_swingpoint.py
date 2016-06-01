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

        # This is a short strategy
        self.direction = strategy_context['strategy']['direction']

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
                 'sphLevel': pd.Series(sphLevel, index=data.exo.index),
                 'splLevel': pd.Series(splLevel, index=data.exo.index),
                 'sphVolume': pd.Series(sphVolume, index=data.exo.index),
                 'splVolume': pd.Series(splVolume, index=data.exo.index),
                 'volumeSeries': pd.Series(volumeArray, index=data.exo.index),
                 'price':  pd.Series(data.exo, index=data.exo.index)
            },
            index=data.exo.index)

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
            sphTreshold_value, splTreshold_value, rules_index, period_median = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            sphTreshold_value, splTreshold_value, rules_index, period_median = params

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

        bearish_breakout_confirmed, bearish_failure_confirmed, bullish_breakout_confirmed, bullish_failure_confirmed = self.calc_entry_rules(
            sp_df)

        if self.direction == 1:
            rules_list = [bullish_breakout_confirmed, bullish_failure_confirmed]

        elif self.direction == -1:
            rules_list = [bearish_breakout_confirmed, bearish_failure_confirmed]


            # Median based trailing stop
        trailing_stop = px.rolling(period_median).median().shift(1)

        # Enry/exit rules
        entry_rule = rules_list[rules_index]

        if self.direction == 1:
            exit_rule = (CrossDown(px, trailing_stop))  # Cross down for longs

        elif self.direction == -1:
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

    def calc_entry_rules(self, sp_df):
        epsilon = 1.0000e-012

        df_sph_level_shift = sp_df.sphLevel.shift(1).values
        df_spl_level_shift = sp_df.splLevel.shift(1).values
        price = sp_df.price.values
        prev_price = sp_df.price.shift(1).values
        num_bars = len(sp_df)


        bullish_breakout_confirmed = (price > df_sph_level_shift) & (
            (price - df_sph_level_shift) >= epsilon)

        # Without volume Confirmed and Suspected are the same rules
        # bullish_breakout_suspected = (sp_df.price > sp_df.sphLevel.shift(1)) & ((sp_df.price - sp_df.sphLevel.shift(1)) >= epsilon) & (sp_df.volumeSeries > sp_df.sphVolume.shift(1))


        bearish_breakout_confirmed = (price < df_spl_level_shift) & (
            (price - df_spl_level_shift) <= -epsilon)

        # Without volume Confirmed and Suspected are the same rules
        # bearish_breakout_suspected = (sp_df.price < sp_df.splLevel.shift(1)) & ((sp_df.price - sp_df.splLevel.shift(1)) <= -epsilon) & (sp_df.volumeSeries <= sp_df.splVolume.shift(1))
        # Days after breakout calc
        ##
        ## Bullish
        ##
        confirmationTimeThresholdBullish = 0  # Days after breakout
        confirmationTimeThresholdBearush = 0  # Days after breakout


        array_bullish_confirm = np.zeros(num_bars)
        array_bearish_confirm = np.zeros(num_bars)

        bullish_breakout_confirmed_prev = np.roll(bullish_breakout_confirmed, 1)
        bearish_breakout_confirmed_prev = np.roll(bearish_breakout_confirmed, 1)

        for i in range(num_bars):
            if bullish_breakout_confirmed_prev[i] == 1 and bullish_breakout_confirmed[i] == 0:
                confirmationTimeThresholdBullish += 1
            elif bullish_breakout_confirmed[i] == 0:
                confirmationTimeThresholdBullish += 1
            elif bullish_breakout_confirmed[i] == 1:
                confirmationTimeThresholdBullish = 0
            array_bullish_confirm[i] = confirmationTimeThresholdBullish

            if bearish_breakout_confirmed_prev[i] == 1 and bearish_breakout_confirmed[i] == 0:
                confirmationTimeThresholdBearush += 1
            elif bearish_breakout_confirmed[i] == 0:
                confirmationTimeThresholdBearush += 1
            elif bearish_breakout_confirmed[i] == 1:
                confirmationTimeThresholdBearush = 0
            array_bearish_confirm[i] = confirmationTimeThresholdBearush


        sp_df['confirmationTimeThresholdBullish'] = pd.Series(array_bullish_confirm, index=sp_df.index)
        sp_df['confirmationTimeThresholdBearish'] = pd.Series(array_bearish_confirm, index=sp_df.index)



        # Failure flags calc
        ##
        ## Bullish
        ##
        bullish_failureflag = 0
        bearish_failureflag = 0

        failureLongLine = prev_price
        failureShortLine = prev_price

        longPenetrationCount = 0
        shortPenetrationCount = 0

        array_bullish_failure = np.zeros(num_bars)
        array_bearish_failure = np.zeros(num_bars)

        for i in range(num_bars):
            #
            # Bullish failures calculation
            #
            if (price[i] < failureLongLine[i]) and (longPenetrationCount <= array_bullish_confirm[i]):
                bullish_failureflag = 1
            elif (longPenetrationCount > sp_df.confirmationTimeThresholdBullish.iat[i]):
                bullish_failureflag = 0
            else:
                longPenetrationCount += 1
            array_bullish_failure[i] = bullish_failureflag

            #
            # Bearish failures calculation
            #
            if (price[i] > failureShortLine[i]) & (shortPenetrationCount <= sp_df.confirmationTimeThresholdBearish.iat[i]):
                bearish_failureflag = 1
            elif (shortPenetrationCount > sp_df.confirmationTimeThresholdBearish.iat[i]):
                bearish_failureflag = 0
            else:
                shortPenetrationCount = shortPenetrationCount + 1

            array_bearish_failure[i] = bearish_failureflag


        sp_df['bullish_failureflag'] = pd.Series(array_bullish_failure, index=sp_df.index)
        sp_df['bearish_failureflag'] = pd.Series(array_bearish_failure, index=sp_df.index)


        bullish_failure_confirmed = (bullish_breakout_confirmed == 1) & (sp_df.bullish_failureflag == 1)

        bearish_failure_confirmed = (bearish_breakout_confirmed == 1) & (sp_df.bearish_failureflag == 1)
        return pd.Series(bearish_breakout_confirmed, index=sp_df.index), \
            pd.Series(bearish_failure_confirmed, index=sp_df.index), \
            pd.Series(bullish_breakout_confirmed, index=sp_df.index), \
            pd.Series(bullish_failure_confirmed, index=sp_df.index)


if __name__ == "__main__":
    #
    #   Run this code only from direct shell execution
    #
    #strategy = StrategyMACrossTrail()
    #equity, stats = strategy.calculate()

    # Do some work
    data, info = matlab.loaddata('../mat/strategy_270225.mat')
    data.plot()