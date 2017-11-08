#
#
#  Automatically generated file 
#        Created at: 2017-01-17 18:29:34.788926
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bearish_Jan17"

STRATEGY_CONTEXT = {
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'exo_name': 'NG_CallSpread',
        'class': StrategySwingPoint,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('sphTreshold', 2, 4, 6, 1), 
            OptParam('splTreshold', 2, 7, 9, 1), 
            OptParamArray('RulesIndex', [2, 3]), 
            OptParam('MedianPeriod', 5, 90, 90, 13), 
        ],
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
