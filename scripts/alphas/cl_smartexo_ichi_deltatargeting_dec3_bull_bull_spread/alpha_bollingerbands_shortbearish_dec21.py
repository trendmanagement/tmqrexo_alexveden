#
#
#  Automatically generated file 
#        Created at: 2016-12-21 12:17:00.090351
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "Bearish_Dec21"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 15, 40, 25), 
            OptParam('BB_K', 2, 17, 22, 1), 
            OptParamArray('RulesIndex', [4, 3]), 
            OptParam('MedianPeriod', 5, 15, 75, 10), 
        ],
        'class': StrategyBollingerBands,
        'exo_name': 'CL_SmartEXO_Ichi_DeltaTargeting_Dec3_Bull_Bull_Spread',
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
}
