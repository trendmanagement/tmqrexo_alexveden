#
#
#  Automatically generated file 
#        Created at: 2017-01-03 09:57:59.931084
#
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "Bearish_Dec21"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'strategy': {
        'class': StrategyBollingerBands,
        'exo_name': 'CL_ContFut',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 4, 15, 1), 
            OptParam('BB_K', 2, 27, 57, 10), 
            OptParamArray('RulesIndex', [3]), 
            OptParam('MedianPeriod', 5, 25, 25, 10), 
        ],
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
}
