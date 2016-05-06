import sys,os
sys.path.append('..')
import unittest
from backtester import matlab, backtester
from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam
from backtester.swarms import SwarmManager, SwarmRanker
from backtester.positionsizing import PositionSizingBase
import pandas as pd
import numpy as np
import scipy

strategyname_global = 'strategy_270225'

class StrategyMACrossTrail(StrategyBase):
    def __init__(self):
        # Initialize parent class
        super().__init__()

        # Define system's name
        self.name = 'MA Crossing with trailing stop'

        # This is a short strategy
        self.direction = -1

        # Define optimized params
        self.opts = [
            #OptParam(name, default_value, min_value, max_value, step)
            OptParam('SlowMAPeriod', 20, 10, 30, 2),
            OptParam('FastMAPeriod', 2, 2, 20, 1),
            OptParam('MedianPeriod', 5, 5, 20, 3)
        ]

        self.initialize()

    def initialize(self):
        #
        #  Loading EXO quotes from .mat file
        #
        strategyname = strategyname_global
        self.data, info = matlab.loaddata('../mat/'+strategyname+'.mat')

        #
        # Estimating transaction costs in base points of price
        #

        # No costs
        #self.costs = pd.Series(0, self.data.index)

        # Flat costs / 1 point of EXO price per side / 2 roundtrip
        self.costs = pd.Series(100.0, self.data.index)

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
        exit_rule = (CrossUp(fast_ma, slow_ma) ) | (CrossUp(px, trailing_stop))

        # Swarm_member_name must be *unique* for every swarm member
        # We use params values for uniqueness
        swarm_member_name = str((period_slow, period_fast, period_median))

        return swarm_member_name, entry_rule, exit_rule

class MyTestCase(unittest.TestCase):
    def test_something(self):
        strategy = StrategyMACrossTrail()

        # Running all parameters permutations in swarm
        swarm = strategy.run_swarm()

        context = {
            'nsystems': 5, # Number of swarm members to pick
        }
        rebalance_time = swarm.index.dayofweek == 0
        ranking_func =  SwarmRanker.highestreturns_14days

        swarm_manager = SwarmManager(rebalancetime=rebalance_time,    # Every week
                             rankerfunc=ranking_func,         # Rank - 14 days returns
                             context=context,                 # Backtester settings / params
                            )

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
