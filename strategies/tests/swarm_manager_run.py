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

from backtester.positionsizing import PositionSizingBase
import pandas as pd
import numpy as np
import scipy


from strategies.strategy_swingpoint import StrategySwingPoint
from strategies.strategy_macross_with_trail import StrategyMACrossTrail

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategySwingPoint,
        'exo_name': '../../mat/strategy_270201.mat',
        'direction': -1,
        'opt_params': [
            #OptParam(name, default_value, min_value, max_value, step)
                        OptParam('sphTreshold', 2, 1, 10, 2),
                        OptParam('splTreshold', 2, 1, 10, 2),
                        OptParam('RulesIndex', 0, 0 , 3, 1),
                        OptParam('MedianPeriod', 5, 5, 20, 3)
        ],
    },
    'swarm': {
        'members_count': 1,
        'ranking_function': SwarmRanker.highestreturns_14days,
        'rebalance_time_function': SwarmRebalance.every_monday,

        'global_filter_function': SwarmFilter.swingpoint_threshold,
        'global_filter_params': {
            'up_factor': 5.0,
            'down_factor': 5.0,
            'period': 5,
        },
        # 'global_filter_function': filter_rolling_mean,
        # 'global_filter_params': {
        #    'ma_period': 100,
        # }
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 0.0,
            'costs_futures': 0.0,
        }
    }
}


swarm_manager = SwarmManager(STRATEGY_CONTEXT)
swarm_manager.run_swarm()
picked_swarm = swarm_manager.pick()
picked_swarm
