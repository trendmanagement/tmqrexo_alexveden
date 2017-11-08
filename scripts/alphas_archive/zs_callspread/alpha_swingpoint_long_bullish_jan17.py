#
#
#  Automatically generated file 
#        Created at: 2017-01-17 11:50:15.987904
#
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bullish_Jan17"

STRATEGY_CONTEXT = {
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
    'strategy': {
        'exo_name': 'ZS_CallSpread',
        'class': StrategySwingPoint,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('sphTreshold', 2, 3, 17, 7), 
            OptParam('splTreshold', 2, 1, 2, 1), 
            OptParamArray('RulesIndex', [0]), 
            OptParam('MedianPeriod', 5, 7, 54, 13), 
        ],
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
}
