#
#
#  Automatically generated file 
#        Created at: 2016-12-13 11:19:05.762952
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bearish_Dec13"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyBollingerBands,
        'exo_name': 'ZC_CallSpread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 42, 42, 10), 
            OptParam('BB_K', 2, 17, 22, 5), 
            OptParamArray('RulesIndex', [0, 1, 3]), 
            OptParam('MedianPeriod', 5, 25, 25, 10), 
        ],
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
