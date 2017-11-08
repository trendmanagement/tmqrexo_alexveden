#
#
#  Automatically generated file 
#        Created at: 2016-12-22 12:18:46.223185
#
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bullish_Dec13"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 12, 12, 10), 
            OptParam('BB_K', 2, 62, 62, 10), 
            OptParamArray('RulesIndex', [6]), 
            OptParam('MedianPeriod', 5, 7, 17, 10), 
        ],
        'exo_name': 'ZN_CallSpread',
        'class': StrategyBollingerBands,
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
