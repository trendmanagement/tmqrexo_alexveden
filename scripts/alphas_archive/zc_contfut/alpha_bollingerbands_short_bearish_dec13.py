#
#
#  Automatically generated file 
#        Created at: 2016-12-13 11:04:59.356468
#
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_bbands import StrategyBollingerBands


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bearish_Dec13"

STRATEGY_CONTEXT = {
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'exo_name': 'ZC_ContFut',
        'class': StrategyBollingerBands,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 10, 10, 5), 
            OptParam('BB_K', 2, 9, 9, 1), 
            OptParamArray('RulesIndex', [20]), 
            OptParam('MedianPeriod', 5, 13, 54, 13), 
        ],
    },
}
