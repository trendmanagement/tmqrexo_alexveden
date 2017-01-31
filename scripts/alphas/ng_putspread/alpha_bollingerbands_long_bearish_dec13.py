#
#
#  Automatically generated file 
#        Created at: 2017-01-07 03:05:05.201628
#
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray


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
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 12, 22, 10), 
            OptParam('BB_K', 2, 22, 52, 30), 
            OptParamArray('RulesIndex', [2]), 
            OptParam('MedianPeriod', 5, 13, 13, 13), 
        ],
        'exo_name': 'NG_PutSpread',
        'class': StrategyBollingerBands,
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
