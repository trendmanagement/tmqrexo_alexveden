#
#
#  Automatically generated file 
#        Created at: 2016-12-19 11:03:37.423589
#
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bearish_Dec13"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'exo_name': 'ZN_PutSpread',
        'class': StrategyBollingerBands,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 32, 32, 10), 
            OptParam('BB_K', 2, 52, 52, 10), 
            OptParamArray('RulesIndex', [4, 5, 18, 18]), 
            OptParam('MedianPeriod', 5, 7, 7, 10), 
        ],
    },
}
