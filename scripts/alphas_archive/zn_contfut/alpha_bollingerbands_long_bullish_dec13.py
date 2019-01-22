#
#
#  Automatically generated file 
#        Created at: 2016-12-19 10:59:41.725310
#
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bullish_Dec13"

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
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 32, 32, 5), 
            OptParam('BB_K', 2, 2, 2, 10), 
            OptParamArray('RulesIndex', [23]), 
            OptParam('MedianPeriod', 5, 15, 50, 5), 
        ],
        'exo_name': 'ZN_ContFut',
        'class': StrategyBollingerBands,
    },
}
