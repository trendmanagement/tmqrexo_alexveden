#
#
#  Automatically generated file 
#        Created at: 2016-12-12 12:08:11.559467
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bi_Short_Dec12"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('BB_Period', 20, 7, 7, 5), 
            OptParam('BB_K', 2, 12, 20, 1), 
            OptParamArray('RulesIndex', [8]), 
            OptParam('MedianPeriod', 5, 5, 20, 5), 
        ],
        'class': StrategyBollingerBands,
        'exo_name': 'CL_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
