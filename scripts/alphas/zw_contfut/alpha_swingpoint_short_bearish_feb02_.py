#
#
#  Automatically generated file 
#        Created at: 2017-02-09 10:14:35.606968
#
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bearish_Feb02_"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('sphTreshold', 2, 8, 11, 1), 
            OptParam('splTreshold', 2, 7, 9, 1), 
            OptParamArray('RulesIndex', [2]), 
            OptParam('MedianPeriod', 5, 52, 52, 13), 
        ],
        'class': StrategySwingPoint,
        'exo_name': 'ZW_ContFut',
    },
}
