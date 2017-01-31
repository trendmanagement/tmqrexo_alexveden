#
#
#  Automatically generated file 
#        Created at: 2016-12-13 14:44:26.757170
#
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bullish_Dec13"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategySwingPoint,
        'exo_name': 'ZC_ContFut',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('sphTreshold', 2, 4, 4, 1), 
            OptParam('splTreshold', 2, 1, 2, 1), 
            OptParamArray('RulesIndex', [3]), 
            OptParam('MedianPeriod', 5, 25, 55, 10), 
        ],
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
}
