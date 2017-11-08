#
#
#  Automatically generated file 
#        Created at: 2017-01-25 12:05:03.204256
#
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bullish_Jan17"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'strategy': {
        'class': StrategyBollingerBands,
        'exo_name': 'ZW_PutSpread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 45, 45, 10), 
            OptParam('BB_K', 2, 10, 10, 5), 
            OptParamArray('RulesIndex', [10, 4, 15]), 
            OptParam('MedianPeriod', 5, 2, 7, 10), 
        ],
    },
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
}
