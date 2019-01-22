#
#
#  Automatically generated file 
#        Created at: 2017-01-16 12:48:16.520852
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bullish_Jan17"

STRATEGY_CONTEXT = {
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'class': StrategySwingPoint,
        'exo_name': 'CL_PutSpread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('sphTreshold', 2, 5, 9, 1), 
            OptParam('splTreshold', 2, 4, 9, 1), 
            OptParamArray('RulesIndex', [2]), 
            OptParam('MedianPeriod', 5, 1, 46, 13), 
        ],
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
}
