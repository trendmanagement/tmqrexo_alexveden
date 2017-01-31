#
#
#  Automatically generated file 
#        Created at: 2016-12-21 13:25:29.863142
#
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "Bearish_Dec21"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
    'strategy': {
        'exo_name': 'CL_PutSpread',
        'class': StrategySwingPoint,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('sphTreshold', 2, 3, 3, 1), 
            OptParam('splTreshold', 2, 2, 2, 1), 
            OptParamArray('RulesIndex', [0, 1, 3]), 
            OptParam('MedianPeriod', 5, 29, 35, 2), 
        ],
    },
}
