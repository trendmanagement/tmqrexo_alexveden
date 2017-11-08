#
#
#  Automatically generated file 
#        Created at: 2017-01-17 11:34:28.804034
#
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bullish_Jan17"

STRATEGY_CONTEXT = {
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'strategy': {
        'class': StrategyBollingerBands,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 2, 32, 10), 
            OptParam('BB_K', 2, 2, 32, 10), 
            OptParamArray('RulesIndex', [10, 17, 24]), 
            OptParam('MedianPeriod', 5, 45, 45, 10), 
        ],
        'exo_name': 'ZS_CallSpread',
    },
}
