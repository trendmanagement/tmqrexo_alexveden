#
#
#  Automatically generated file 
#        Created at: 2016-12-22 09:32:28.219957
#
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bullish_Dec13"

STRATEGY_CONTEXT = {
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'exo_name': 'ZS_CallSpread',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('sphTreshold', 2, 3, 8, 3), 
            OptParam('splTreshold', 2, 1, 6, 5), 
            OptParamArray('RulesIndex', [1, 2, 3]), 
            OptParam('MedianPeriod', 5, 15, 45, 30), 
        ],
        'class': StrategySwingPoint,
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
