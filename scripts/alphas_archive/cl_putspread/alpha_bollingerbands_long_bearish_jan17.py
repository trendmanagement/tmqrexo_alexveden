#
#
#  Automatically generated file 
#        Created at: 2017-01-17 09:41:41.599112
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bearish_Jan17"

STRATEGY_CONTEXT = {
    'strategy': {
        'exo_name': 'CL_PutSpread',
        'class': StrategyBollingerBands,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 12, 12, 10), 
            OptParam('BB_K', 2, 22, 32, 10), 
            OptParamArray('RulesIndex', [0, 14]), 
            OptParam('MedianPeriod', 5, 33, 145, 10), 
        ],
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
