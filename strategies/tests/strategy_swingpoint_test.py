import unittest
import sys,os
sys.path.append('..')
from backtester import matlab, backtester
from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam
from backtester.swarms.manager import SwarmManager
from backtester.swarms.ranking import SwarmRanker
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.filters import SwarmFilter
from backtester.costs import CostsManagerEXOFixed

import pandas as pd
import numpy as np
import scipy

import time

from strategies.strategy_swingpoint import StrategySwingPoint

import logging
logger = logging.getLogger()


STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategySwingPoint,
        'exo_name': './data/strategy_2010348.mat',
        'direction': -1,
        'opt_params': [
                # OptParam(name, default_value, min_value, max_value, step)
                OptParam('sphTreshold', 2, 10, 14, 2),
                OptParam('splTreshold', 2, 10, 14, 2),
                OptParam('RulesIndex', 0, 0, 1, 1),
                OptParam('MedianPeriod', 5, 5, 20, 3)
            ],
    },
    'swarm': {
        'members_count': 5,
        'ranking_function': SwarmRanker.highestreturns_14days,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'global_filter_function': SwarmFilter.swingpoint_threshold,
        'global_filter_params': {
            'up_factor': 3.0,
            'down_factor': 10.0,
            'period': 1,
        }
    },
    'costs':{
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        }
    }
}

class StrategySwingPointTestCase(unittest.TestCase):
    def test_swp_performance(self):
        def swingpoints(sphThreshold, splThreshold, data):

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

            OPEN = 0
            HIGH = 1
            LOW = 2
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
                    'price': pd.Series(data.exo, index=data.exo.index)
                },
                index=data.exo.index)

        strategy = StrategySwingPoint(STRATEGY_CONTEXT)

        t = time.process_time()
        # do some stuff

        orig_df = strategy.swingpoints(sphThreshold=10, splThreshold=10, data=strategy.data)
        elapsed_time = time.process_time() - t
        print("Original SWP code time: {0}".format(elapsed_time*10))

        t = time.process_time()
        for i in range(10):
            new_df = swingpoints(sphThreshold=10, splThreshold=10, data=strategy.data)
        elapsed_time = time.process_time() - t
        print("Optimized SWP code time: {0}".format(elapsed_time))

        self.assertEqual(0, (orig_df.sphLevel-new_df.sphLevel).sum())
        self.assertEqual(0, (orig_df.splLevel - new_df.splLevel).sum())
        self.assertEqual(0, (orig_df.sphVolume - new_df.sphVolume).sum())
        self.assertEqual(0, (orig_df.splVolume - new_df.splVolume).sum())
        self.assertEqual(0, (orig_df.volumeSeries - new_df.volumeSeries).sum())
        self.assertEqual(0, (orig_df.price - new_df.price).sum())

        self.assertEqual(False, True)

    def test_entry_rules_performance(self):
        def calc_entry_rules(sp_df):

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
            return bearish_breakout_confirmed, bearish_failure_confirmed, bullish_breakout_confirmed, bullish_failure_confirmed

        strategy = StrategySwingPoint(STRATEGY_CONTEXT)

        sp_df = strategy.swingpoints(sphThreshold=10, splThreshold=10, data=strategy.data)

        t = time.process_time()
        # do some stuff
        bearish_breakout_confirmed, bearish_failure_confirmed, bullish_breakout_confirmed, bullish_failure_confirmed = strategy.calc_entry_rules(sp_df)
        elapsed_time = time.process_time() - t
        print("Original SWP rules code time: {0}".format(elapsed_time * 10))

        t = time.process_time()
        for i in range(10):
            bearish_breakout_confirmed1, bearish_failure_confirmed1, bullish_breakout_confirmed1, bullish_failure_confirmed1 = calc_entry_rules(
                sp_df)
        elapsed_time = time.process_time() - t
        print("Optimized SWP rules code time: {0}".format(elapsed_time))

        for i in range(len(sp_df)):
            self.assertEqual(bearish_breakout_confirmed[i], bearish_breakout_confirmed1[i])
            self.assertEqual(bearish_failure_confirmed[i], bearish_failure_confirmed1[i])
            self.assertEqual(bullish_breakout_confirmed[i], bullish_breakout_confirmed1[i])
            self.assertEqual(bullish_failure_confirmed[i], bullish_failure_confirmed1[i])


        self.assertEqual(False, True)


if __name__ == '__main__':
    unittest.main()
