#
#
#  Automatically generated file 
#        Created at: 2017-01-17 06:55:25.753573
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray
from strategies.strategy_bbands import StrategyBollingerBands


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bearish_Jan17"

STRATEGY_CONTEXT = {
    'strategy': {
        'exo_name': 'CL_CallSpread',
        'class': StrategyBollingerBands,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 12, 32, 10), 
            OptParam('BB_K', 2, 12, 32, 10), 
            OptParamArray('RulesIndex', [0, 2, 12]), 
            OptParam('MedianPeriod', 5, 1, 45, 10), 
        ],
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
}
