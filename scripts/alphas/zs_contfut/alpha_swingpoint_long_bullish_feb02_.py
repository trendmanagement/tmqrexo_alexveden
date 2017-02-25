#
#
#  Automatically generated file 
#        Created at: 2017-02-07 17:32:32.730105
#
from strategies.strategy_swingpoint import StrategySwingPoint
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bullish_Feb02_"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
    'strategy': {
        'class': StrategySwingPoint,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('sphTreshold', 2, 2, 5, 1), 
            OptParam('splTreshold', 2, 1, 6, 1), 
            OptParamArray('RulesIndex', [1, 2, 3]), 
            OptParam('MedianPeriod', 5, 5, 25, 5), 
        ],
        'exo_name': 'ZS_ContFut',
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
