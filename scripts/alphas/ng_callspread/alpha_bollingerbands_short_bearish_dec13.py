#
#
#  Automatically generated file 
#        Created at: 2016-12-14 10:54:27.568109
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bearish_Dec13"

STRATEGY_CONTEXT = {
    'strategy': {
        'exo_name': 'NG_CallSpread',
        'class': StrategyBollingerBands,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 2, 22, 10), 
            OptParam('BB_K', 2, 22, 32, 10), 
            OptParamArray('RulesIndex', [23, 15]), 
            OptParam('MedianPeriod', 5, 13, 54, 13), 
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
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
