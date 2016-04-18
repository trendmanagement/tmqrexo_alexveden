#!/usr/bin/python

import sys,os
sys.path.append('..')
from backtester import matlab, backtester
from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam
import pandas as pd
import numpy as np
import scipy


class StrategyMACrossTrail(StrategyBase):
    def __init__(self):
        # Initialize parent class
        super().__init__()

        # Define system's name
        self.name = 'MA Crossing with trailing stop'

        # Define optimized params
        self.opts = [
            #OptParam(name, default_value, min_value, max_value, step)
            OptParam('SlowMAPeriod', 50, 50, 100, 2),
            OptParam('FastMAPeriod', 10, 10, 50, 2),
            OptParam('MedianPeriod', 15, 5, 20, 5)
        ]

        self.initialize()

    def initialize(self):
        #
        #  Loading EXO quotes from .mat file
        #
        strategyname = 'strategy_270225'
        self.data, info = matlab.loaddata('../mat/'+strategyname+'.mat')

    def calculate(self, params=None):
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
            period_slow, period_fast, period_median = self.default_opts()
        else:
            # Unpacking optimization params
            #  in order in self.opts definition
            period_slow, period_fast, period_median = params

        #
        #
        # Indicator calculation
        #

        # Defining EXO price
        px = self.data.exo
        slow_ma = px.rolling(period_slow) .mean()
        fast_ma = px.rolling(period_fast).mean()
        # Median based trailing stop
        trailing_stop = px.rolling(period_median).median().shift(1)

        # Enry/exit rules
        short_entry = CrossDown(fast_ma, slow_ma)
        short_exit = (CrossUp(fast_ma, slow_ma) ) | (CrossUp(px, trailing_stop))

        # Backtesting routine
        direction = -1
        pl, inposition = backtester.backtest(d, short_entry, short_exit, direction )
        equity, stats = backtester.stats(pl, inposition)

        return equity, stats


if __name__ == "__main__":
    #
    #   Run this code only from direct shell execution
    #
    strategy = StrategyMACrossTrail()
    equity, stats = strategy.calculate()

    # Do some work