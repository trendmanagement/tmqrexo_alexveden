#
#
#  Automatically generated file 
#        Created at: 2017-01-16 12:50:04.751642
#
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bullish_Jan17"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('sphTreshold', 2, 2, 6, 4), 
            OptParam('splTreshold', 2, 2, 9, 7), 
            OptParamArray('RulesIndex', [0, 3]), 
            OptParam('MedianPeriod', 5, 1, 46, 13), 
        ],
        'exo_name': 'CL_ContFut',
        'class': StrategySwingPoint,
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
}
