#
#
#  Automatically generated file 
#        Created at: 2016-12-16 11:37:12.230500
#
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bearish_Dec13"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'strategy': {
        'exo_name': 'ZS_CallSpread',
        'class': StrategySwingPoint,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('sphTreshold', 2, 1, 1, 1), 
            OptParam('splTreshold', 2, 10, 10, 1), 
            OptParamArray('RulesIndex', [0, 3]), 
            OptParam('MedianPeriod', 5, 15, 45, 30), 
        ],
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
