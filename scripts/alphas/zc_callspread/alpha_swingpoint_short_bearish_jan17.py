#
#
#  Automatically generated file 
#        Created at: 2017-01-19 22:17:18.478851
#
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bearish_Jan17"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategySwingPoint,
        'exo_name': 'ZC_CallSpread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('sphTreshold', 2, 1, 3, 1), 
            OptParam('splTreshold', 2, 1, 3, 1), 
            OptParamArray('RulesIndex', [3]), 
            OptParam('MedianPeriod', 5, 30, 37, 3), 
        ],
    },
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
}
