#
#
#  Automatically generated file 
#        Created at: 2016-12-12 11:53:37.156159
#
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bullish_Dec12"

STRATEGY_CONTEXT = {
    'strategy': {
        'exo_name': 'CL_PutSpread',
        'class': StrategyBollingerBands,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 32, 42, 5), 
            OptParam('BB_K', 2, 7, 42, 5), 
            OptParamArray('RulesIndex', [23, 8, 9]), 
            OptParam('MedianPeriod', 5, 15, 45, 10), 
        ],
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
