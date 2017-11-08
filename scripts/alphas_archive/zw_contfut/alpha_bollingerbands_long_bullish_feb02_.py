#
#
#  Automatically generated file 
#        Created at: 2017-02-09 10:06:02.321063
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bullish_Feb02_"

STRATEGY_CONTEXT = {
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
    'strategy': {
        'exo_name': 'ZW_ContFut',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 25, 25, 10), 
            OptParam('BB_K', 2, 10, 10, 5), 
            OptParamArray('RulesIndex', [18, 17, 16, 3, 2]), 
            OptParam('MedianPeriod', 5, 7, 37, 10), 
        ],
        'class': StrategyBollingerBands,
    },
}
