#
#
#  Automatically generated file 
#        Created at: 2016-12-13 11:46:18.565824
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bearish_Dec13"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 5, 25, 5), 
            OptParam('BB_K', 2, 2, 10, 1), 
            OptParamArray('RulesIndex', [22]), 
            OptParam('MedianPeriod', 5, 35, 85, 10), 
        ],
        'exo_name': 'ZC_PutSpread',
        'class': StrategyBollingerBands,
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
