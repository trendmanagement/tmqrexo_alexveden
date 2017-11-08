#
#
#  Automatically generated file 
#        Created at: 2016-12-15 10:26:45.645768
#
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_swingpoint import StrategySwingPoint


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bullish_Dec13"

STRATEGY_CONTEXT = {
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'class': StrategySwingPoint,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('sphTreshold', 2, 1, 1, 1), 
            OptParam('splTreshold', 2, 1, 2, 1), 
            OptParamArray('RulesIndex', [1]), 
            OptParam('MedianPeriod', 5, 2, 15, 1), 
        ],
        'exo_name': 'ZW_PutSpread',
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
