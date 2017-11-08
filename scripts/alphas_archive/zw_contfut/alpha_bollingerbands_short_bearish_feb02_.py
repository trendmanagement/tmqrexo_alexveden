#
#
#  Automatically generated file 
#        Created at: 2017-02-09 10:07:24.557486
#
from backtester.strategy import OptParam
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bearish_Feb02_"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 5, 35, 10), 
            OptParam('BB_K', 2, 10, 10, 5), 
            OptParamArray('RulesIndex', [12, 19, 25]), 
            OptParam('MedianPeriod', 5, 7, 7, 10), 
        ],
        'exo_name': 'ZW_ContFut',
        'class': StrategyBollingerBands,
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
}
