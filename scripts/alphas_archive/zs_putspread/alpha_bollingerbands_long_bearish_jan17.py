#
#
#  Automatically generated file 
#        Created at: 2017-01-17 11:36:43.401084
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from strategies.strategy_bbands import StrategyBollingerBands


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bearish_Jan17"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 22, 22, 10), 
            OptParam('BB_K', 2, 12, 12, 10), 
            OptParamArray('RulesIndex', [12, 14, 15]), 
            OptParam('MedianPeriod', 5, 45, 45, 10), 
        ],
        'class': StrategyBollingerBands,
        'exo_name': 'ZS_PutSpread',
    },
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
}
