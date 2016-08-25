from backtester import matlab, backtester
from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam, OptParamArray
from backtester.swarms.manager import SwarmManager
from backtester.swarms.ranking import SwarmRanker
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.filters import SwarmFilter
from backtester.costs import CostsManagerEXOFixed
from backtester.exoinfo import EXOInfo

import pandas as pd
import numpy as np
import scipy


from strategies.strategy_renko_no_exit_on_patterns import StrategyRenkoPatterns_no_exit_on_patterns

STRATEGY_NAME = "Renko"

STRATEGY_SUFFIX = 'no-exit-on-patterns'

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyRenkoPatterns_no_exit_on_patterns,
        'exo_name': 'strategy_340240',
        'opt_params': [
            # OptParam(name, default_value, min_value, max_value, step)
            OptParamArray('Direction', [1]),
            OptParam('BoxSize', 500, 100, 1000, 50),
            OptParam('MoveCount', 2, 2, 2, 1),
            OptParamArray('RulesIndex', np.arange(9)),
            OptParam('MedianPeriod', 5, 1, 20, 2)

        ],
    },
    'swarm': {
        'members_count': 5,
        'ranking_function': SwarmRanker.highestreturns_universal,
        'ranking_params': {
            # 'ranking_type' - global ranking mode
            # 'returns' - main ranking function based on highest returns N days
            # 'relstr_ratio' - relative strength (equity / MA(equity)) (has negative equity BUG!)
            # 'relstr_delta' - relative strength (equity - MA(equity))
            'ranking_type': 'returns',

            # Used for 'ranking_type' = 'relstr'
            'ranking_relstr_ma_period': 21,
            'ranking_relstr_upperbound': 1.5,
            'ranking_relstr_lowerbound': 0.01,

            # Used for 'ranking_type' = 'returns'
            # Ranking function exta parameters (main ranking metric period)
            'ranking_returns_period': 4,

            # Ignoring all members which equity less than it's MovingAverage({ignore_eqty_less_ma_period})
            # 'ignore_eqty_less_ma': True,                    # Comment the line to turn off
            'ignore_eqty_less_ma_period': 90,  # Equity Moving Average period

            # Ignoring all members which equity less than TOP swarmmembers quantile
            # 'ignore_eqty_less_top_quantile': True,          # Comment the line to turn off
            'ignore_eqty_less_top_quantile_threshold': 0.5,  # Ignore all members less than 0.9 quantile

            # Ignoring all swarm members wich have negative MA slope
            # 'ignore_eqty_with_negative_ma_slope': True,     # Comment the line to turn off
            'ignore_eqty_with_negative_ma_period': 90,  # Period of moving average
            'ignore_eqty_with_negative_ma_slope_period': 5,  # Slope lookback filter = MA-MA[-slope_lookback] <= 0

            # Ignoring all swarm members when the change of AvgSwarm equity is negative
            # 'ignore_if_avg_swarm_negative_change': True,      # Comment the line to turn off
            'ignore_if_avg_swarm_negative_change_period': 14,  # AvgSwarm change period

        },
        'rebalance_time_function': SwarmRebalance.every_friday,
        # SwarmFilter.swingpoint_daily - original TMQR Swingpoint logics from Matlab
        # SwarmFilter.volatility_chandelier - Alex's volatility based logic (old name: SwarmFilter.swingpoint_threshold)
        'global_filter_function': SwarmFilter.volatility_chandelier,
        'global_filter_params': {
            'up_factor': 5.0,
            'down_factor': 15.0,
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