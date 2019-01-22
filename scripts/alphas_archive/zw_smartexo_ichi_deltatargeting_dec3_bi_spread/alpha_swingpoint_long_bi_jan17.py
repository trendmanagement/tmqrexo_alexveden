#
#
#  Automatically generated file 
#        Created at: 2017-01-25 12:30:15.427326
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bi_Jan17"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('sphTreshold', 2, 1, 3, 1), 
            OptParam('splTreshold', 2, 3, 3, 1), 
            OptParamArray('RulesIndex', [1]), 
            OptParam('MedianPeriod', 5, 52, 52, 13), 
        ],
        'class': StrategySwingPoint,
        'exo_name': 'ZW_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
    },
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
