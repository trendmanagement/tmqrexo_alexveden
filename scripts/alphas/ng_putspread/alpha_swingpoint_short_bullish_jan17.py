#
#
#  Automatically generated file 
#        Created at: 2017-01-17 18:25:47.134494
#
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bullish_Jan17"

STRATEGY_CONTEXT = {
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'exo_name': 'NG_PutSpread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('sphTreshold', 2, 1, 6, 1), 
            OptParam('splTreshold', 2, 1, 9, 1), 
            OptParamArray('RulesIndex', [3]), 
            OptParam('MedianPeriod', 5, 3, 90, 13), 
        ],
        'class': StrategySwingPoint,
    },
}
