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
    def __init__(self, strategy_context):
        # Initialize parent class
        super().__init__(strategy_context)

        # Define system's name
        self.name = 'MA Crossing with trailing stop'

        self.check_context()

        # This is a short strategy
        self.direction = strategy_context['strategy']['direction']

        # Define optimized params
        self.opts = strategy_context['strategy']['opt_params']

        self.exo_name = strategy_context['strategy']['exo_name']

        self.initialize()
    def check_context(self):
        #
        # Do strategy specific checks
        #
        pass


    def initialize(self):
        #
        #  Loading EXO quotes from .mat file
        #
        self.data, info = matlab.loaddata('../mat/' + self.exo_name + '.mat')

        #
        # Estimating transaction costs in base points of price
        #

        # No costs
        self.costs = pd.Series(0, self.data.index)

        # Flat costs / 1 point of EXO price per side / 2 roundtrip
        # self.costs = pd.Series(12.0, self.data.index)

        # Dynamic costs (we could utilize dynamic costs models)
        #  Like slippage calculation on bid/ask data / etc
        # Some meta code (just in my imagination)
        # costmanager = CostManager('EXO.Ticker').LoadSlippageFromDB('2000-01-01', now)
        # self.costs = costmanager.getslippage() + pd.Series(0.1, self.data.index) # Slippage + commission

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

        # Calculate position size adjusted to volatility of EXO
        # Dollar risk per 1 volatility unit
        risk_perunit = 100
        risk_vola_period = 100

        # Calculate volatility unit
        # In this case we use 10-period rolling median of EXO changes
        vola = abs(px.diff()).rolling(risk_vola_period).median()
        # We want to risk 100$ per 1 volatility unit
        #
        # This type of position sizing used for calibration of swarm members
        # After swarm generation and picking we will use portfolio based MM by Van Tharp
        # Tailored for portfolio size and risks of particular client
        return risk_perunit / vola

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

        # Defining EXO price
        px = self.data.exo

        #
        #
        # Indicator calculation
        #
        #
        slow_ma = px.rolling(period_slow).mean()
        fast_ma = px.rolling(period_fast).mean()
        # Median based trailing stop
        trailing_stop = px.rolling(period_median).median().shift(1)

        # Enry/exit rules
        entry_rule = CrossDown(fast_ma, slow_ma)
        exit_rule = (CrossUp(fast_ma, slow_ma)) | (CrossUp(px, trailing_stop))

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = self.get_member_name(params)

        return swarm_member_name, entry_rule, exit_rule

if __name__ == "__main__":
    #
    #   Run this code only from direct shell execution
    #
    #strategy = StrategyMACrossTrail()
    #equity, stats = strategy.calculate()

    # Do some work
    data, info = matlab.loaddata('../mat/strategy_270225.mat')
    data.plot()