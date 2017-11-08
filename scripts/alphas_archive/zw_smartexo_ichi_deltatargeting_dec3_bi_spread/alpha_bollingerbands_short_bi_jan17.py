#
#
#  Automatically generated file 
#        Created at: 2017-01-25 12:09:55.879201
#
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bi_Jan17"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyBollingerBands,
        'exo_name': 'ZW_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 5, 45, 10), 
            OptParam('BB_K', 2, 10, 90, 20), 
            OptParamArray('RulesIndex', [8]), 
            OptParam('MedianPeriod', 5, 12, 22, 10), 
        ],
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
