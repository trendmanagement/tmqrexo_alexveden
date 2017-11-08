#
#
#  Automatically generated file 
#        Created at: 2016-12-19 11:55:19.560340
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bullish_Dec13"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'strategy': {
        'exo_name': 'ZN_CallSpread',
        'class': StrategySwingPoint,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('sphTreshold', 2, 1, 1, 1), 
            OptParam('splTreshold', 2, 5, 5, 4), 
            OptParamArray('RulesIndex', [3]), 
            OptParam('MedianPeriod', 5, 45, 45, 10), 
        ],
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
