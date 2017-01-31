#
#
#  Automatically generated file 
#        Created at: 2016-12-20 10:07:43.854157
#
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bullish_Dec13"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('sphTreshold', 2, 9, 11, 1), 
            OptParam('splTreshold', 2, 1, 2, 1), 
            OptParamArray('RulesIndex', [3]), 
            OptParam('MedianPeriod', 5, 5, 5, 5), 
        ],
        'exo_name': 'CL_ContFut',
        'class': StrategySwingPoint,
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
}
