#
#
#  Automatically generated file 
#        Created at: 2016-12-20 10:13:25.639896
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bullish_Dec13"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategySwingPoint,
        'exo_name': 'CL_ContFut',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('sphTreshold', 2, 4, 7, 3), 
            OptParam('splTreshold', 2, 9, 9, 7), 
            OptParamArray('RulesIndex', [1, 3]), 
            OptParam('MedianPeriod', 5, 25, 25, 10), 
        ],
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
