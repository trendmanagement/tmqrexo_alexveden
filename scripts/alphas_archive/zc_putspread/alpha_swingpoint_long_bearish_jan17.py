#
#
#  Automatically generated file 
#        Created at: 2017-01-19 22:25:17.900231
#
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bearish_Jan17"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
    'strategy': {
        'exo_name': 'ZC_PutSpread',
        'class': StrategySwingPoint,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('sphTreshold', 2, 1, 3, 1), 
            OptParam('splTreshold', 2, 1, 3, 1), 
            OptParamArray('RulesIndex', [0]), 
            OptParam('MedianPeriod', 5, 3, 15, 3), 
        ],
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
