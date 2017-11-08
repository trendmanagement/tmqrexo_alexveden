#
#
#  Automatically generated file 
#        Created at: 2016-12-15 09:58:13.170283
#
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bullish_Dec13"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
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
            OptParam('BB_Period', 20, 35, 55, 10), 
            OptParam('BB_K', 2, 15, 55, 10), 
            OptParamArray('RulesIndex', [4, 17, 5]), 
            OptParam('MedianPeriod', 5, 15, 35, 10), 
        ],
        'class': StrategyBollingerBands,
        'exo_name': 'ZW_PutSpread',
    },
}
