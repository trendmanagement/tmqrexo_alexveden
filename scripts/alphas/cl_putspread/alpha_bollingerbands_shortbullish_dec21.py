#
#
#  Automatically generated file 
#        Created at: 2016-12-21 12:24:13.047269
#
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "Bullish_Dec21"

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
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 32, 42, 5), 
            OptParam('BB_K', 2, 7, 42, 5), 
            OptParamArray('RulesIndex', [23, 8, 9]), 
            OptParam('MedianPeriod', 5, 15, 45, 10), 
        ],
        'exo_name': 'CL_PutSpread',
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
