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

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategySwingPoint,
        'exo_name': 'strategy_270225',
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
        'rebalance_time_function': SwarmRebalance.every_monday,
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


swarm_manager = SwarmManager(STRATEGY_CONTEXT)
swarm_manager.run_swarm()
picked_swarm = swarm_manager.pick()
picked_swarm
