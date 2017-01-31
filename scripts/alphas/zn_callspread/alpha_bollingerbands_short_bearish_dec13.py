#
#
#  Automatically generated file 
#        Created at: 2016-12-19 10:55:15.902918
#
from backtester.strategy import OptParamArray
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bearish_Dec13"

STRATEGY_CONTEXT = {
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 12, 12, 10), 
            OptParam('BB_K', 2, 2, 12, 10), 
            OptParamArray('RulesIndex', [7]), 
            OptParam('MedianPeriod', 5, 2, 3, 1), 
        ],
        'exo_name': 'ZN_CallSpread',
        'class': StrategyBollingerBands,
    },
}
