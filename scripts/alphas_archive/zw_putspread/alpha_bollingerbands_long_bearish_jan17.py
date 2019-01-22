#
#
#  Automatically generated file 
#        Created at: 2017-01-25 12:02:25.100683
#
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from strategies.strategy_bbands import StrategyBollingerBands


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bearish_Jan17"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
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
            OptParam('BB_Period', 20, 15, 15, 10), 
            OptParam('BB_K', 2, 10, 10, 5), 
            OptParamArray('RulesIndex', [9, 3, 5]), 
            OptParam('MedianPeriod', 5, 2, 25, 10), 
        ],
        'exo_name': 'ZW_PutSpread',
        'class': StrategyBollingerBands,
    },
}
