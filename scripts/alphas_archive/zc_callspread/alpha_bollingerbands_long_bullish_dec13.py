#
#
#  Automatically generated file 
#        Created at: 2016-12-13 11:16:02.653988
#
from backtester.strategy import OptParam
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParamArray
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bullish_Dec13"

STRATEGY_CONTEXT = {
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'strategy': {
        'class': StrategyBollingerBands,
        'exo_name': 'ZC_CallSpread',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 42, 42, 10), 
            OptParam('BB_K', 2, 22, 22, 5), 
            OptParamArray('RulesIndex', [22, 16, 17]), 
            OptParam('MedianPeriod', 5, 25, 25, 10), 
        ],
    },
}
