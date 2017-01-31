#
#
#  Automatically generated file 
#        Created at: 2016-12-12 12:37:19.883434
#
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from strategies.strategy_swingpoint import StrategySwingPoint


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bullish_Dec122016"

STRATEGY_CONTEXT = {
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'strategy': {
        'exo_name': 'CL_PutSpread',
        'class': StrategySwingPoint,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('sphTreshold', 2, 1, 1, 1), 
            OptParam('splTreshold', 2, 2, 5, 1), 
            OptParamArray('RulesIndex', [3]), 
            OptParam('MedianPeriod', 5, 20, 35, 5), 
        ],
    },
}
