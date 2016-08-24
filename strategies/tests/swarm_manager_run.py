import sys,os
sys.path.append('..')
from backtester import matlab, backtester
from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam, OptParamArray
from backtester.swarms.manager import SwarmManager
from backtester.swarms.ranking import SwarmRanker
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.filters import SwarmFilter
from backtester.costs import CostsManagerEXOFixed

from backtester.positionsizing import PositionSizingBase
import pandas as pd
import numpy as np
import scipy


from strategies.strategy_swingpoint import StrategySwingPoint
from strategies.strategy_macross_with_trail import StrategyMACrossTrail

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategySwingPoint,
        'exo_name': '../../mat/strategy_270225.mat',
        'direction': 0,
        'opt_params': [
            # OptParam(name, default_value, min_value, max_value, step)
            OptParamArray('Direction', [-1]),
            OptParam('sphTreshold', 2, 1, 5, 2),
            OptParam('splTreshold', 2, 1, 5, 2),
            # bearish_breakout_confirmed, bearish_failure_confirmed, bullish_breakout_confirmed, bullish_failure_confirmed
            OptParamArray('RulesIndex', [0]),
            OptParam('MedianPeriod', 5, 5, 9, 3)
        ],
    },
    'swarm': {
        'members_count': 5,
        'ranking_function': SwarmRanker.highestreturns_universal,
        'ranking_params': {
            # Ranking function exta parameters (main ranking metric period)
            'eqty_returns_period': 14,

            # Ignoring all members which equity less than it's MovingAverage({ignore_eqty_less_ma_period})
            'ignore_eqty_less_ma': True,  # Comment the line to turn off
            'ignore_eqty_less_ma_period': 90,  # Equity Moving Average period

            # Ignoring all members which equity less than TOP swarmmembers quantile
            'ignore_eqty_less_top_quantile': True,  # Comment the line to turn off
            'ignore_eqty_less_top_quantile_threshold': 0.9,  # Ignore all members less than 0.9 quantile

            # Ignoring all swarm members wich have negative MA slope
            'ignore_eqty_with_negative_ma_slope': True,  # Comment the line to turn off
            'ignore_eqty_with_negative_ma_period': 90,  # Period of moving average
            'ignore_eqty_with_negative_ma_slope_period': 5,  # Slope lookback filter = MA-MA[-slope_lookback] <= 0

            # Ignoring all swarm members when the change of AvgSwarm equity is negative
            'ignore_if_avg_swarm_negative_change': True,  # Comment the line to turn off
            'ignore_if_avg_swarm_negative_change_period': 14,  # AvgSwarm change period

        },
        'rebalance_time_function': SwarmRebalance.every_friday,

        'global_filter_function': SwarmFilter.swingpoint_threshold,
        'global_filter_params': {
            'up_factor': 10.0,
            'down_factor': 10.0,
            'period': 5,
        },
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        }
    }
}


swarm_manager = SwarmManager(STRATEGY_CONTEXT)
swarm_manager.run_swarm()
picked_swarm = swarm_manager.pick()
picked_swarm
