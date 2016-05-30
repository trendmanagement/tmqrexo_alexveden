import sys,os
sys.path.append('..')
from backtester import matlab, backtester
from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam
from backtester.swarms.manager import SwarmManager
from backtester.swarms.ranking import SwarmRanker
from backtester.swarms.rebalancing import rebalance_every_monday, rebalance_norebalance
from backtester.swarms.filters import swingpoint_filter_threshold
from backtester.costs import CostsManagerZeroCosts

from backtester.positionsizing import PositionSizingBase
import pandas as pd
import numpy as np
import scipy


from strategies.strategy_macross_with_trail import StrategyMACrossTrail

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyMACrossTrail,
        'exo_name': 'strategy_270225',
        'direction': -1,
        'opt_params': [
                #OptParam(name, default_value, min_value, max_value, step)
                OptParam('SlowMAPeriod', 20, 10, 30, 2),
                OptParam('FastMAPeriod', 2, 2, 20, 1),
                OptParam('MedianPeriod', 5, 5, 20, 3)
            ],
    },
    'swarm': {
        'members_count': 5,
        'ranking_function': SwarmRanker.highestreturns_14days,
        'rebalance_time_function': rebalance_norebalance,
        #'global_filter_function': swingpoint_filter_threshold,
        'global_filter_params': {
            'up_factor': 3.0,
            'down_factor': 10.0,
            'period': 10,
        }
    },
    'costs':{
        'manager': CostsManagerZeroCosts,
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