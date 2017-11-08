#
#
#  Automatically generated file 
#        Created at: 2016-12-13 11:40:45.453068
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bearish_Dec13_2"

STRATEGY_CONTEXT = {
    'strategy': {
        'exo_name': 'ZC_ContFut',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 10, 10, 20), 
            OptParam('BB_K', 2, 20, 30, 3), 
            OptParamArray('RulesIndex', [1, 22]), 
            OptParam('MedianPeriod', 5, 20, 53, 13), 
        ],
        'class': StrategyBollingerBands,
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
