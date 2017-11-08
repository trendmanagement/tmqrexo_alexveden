#
#
#  Automatically generated file 
#        Created at: 2017-01-25 12:06:49.487926
#
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bi_Jan17"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
    'strategy': {
        'class': StrategyBollingerBands,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 15, 64, 10), 
            OptParam('BB_K', 2, 10, 10, 20), 
            OptParamArray('RulesIndex', [0]), 
            OptParam('MedianPeriod', 5, 12, 22, 10), 
        ],
        'exo_name': 'ZW_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
}
