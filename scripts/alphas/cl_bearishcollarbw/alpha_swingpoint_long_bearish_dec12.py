#
#
#  Automatically generated file 
#        Created at: 2016-12-12 10:57:21.928578
#
from backtester.strategy import OptParamArray
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bearish_Dec12"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('sphTreshold', 2, 3, 3, 1), 
            OptParam('splTreshold', 2, 6, 6, 1), 
            OptParamArray('RulesIndex', [1, 3]), 
            OptParam('MedianPeriod', 5, 35, 95, 20), 
        ],
        'class': StrategySwingPoint,
        'exo_name': 'CL_BearishCollarBW',
    },
}
