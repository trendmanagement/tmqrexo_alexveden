#
#
#  Automatically generated file 
#        Created at: 2016-12-14 11:29:36.485157
#
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bullish_Dec13"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyBollingerBands,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 42, 42, 10), 
            OptParam('BB_K', 2, 32, 32, 10), 
            OptParamArray('RulesIndex', [10, 24, 0, 22]), 
            OptParam('MedianPeriod', 5, 26, 26, 13), 
        ],
        'exo_name': 'NG_PutSpread',
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
}
