#
#
#  Automatically generated file 
#        Created at: 2016-12-14 15:17:07.155073
#
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bi_Dec13"

STRATEGY_CONTEXT = {
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'strategy': {
        'exo_name': 'NG_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('sphTreshold', 2, 1, 5, 4), 
            OptParam('splTreshold', 2, 2, 2, 1), 
            OptParamArray('RulesIndex', [2]), 
            OptParam('MedianPeriod', 5, 5, 15, 5), 
        ],
        'class': StrategySwingPoint,
    },
}
