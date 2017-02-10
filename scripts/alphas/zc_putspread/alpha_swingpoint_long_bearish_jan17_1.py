#
#
#  Automatically generated file 
#        Created at: 2017-01-19 22:28:40.130431
#
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bearish_Jan17_1"

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
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('sphTreshold', 2, 1, 7, 1), 
            OptParam('splTreshold', 2, 1, 3, 1), 
            OptParamArray('RulesIndex', [1]), 
            OptParam('MedianPeriod', 5, 3, 15, 3), 
        ],
        'exo_name': 'ZC_PutSpread',
        'class': StrategySwingPoint,
    },
}
