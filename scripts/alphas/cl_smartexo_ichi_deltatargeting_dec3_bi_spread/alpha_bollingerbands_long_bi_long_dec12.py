#
#
#  Automatically generated file 
#        Created at: 2016-12-21 12:00:40.256868
#
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bi_Long_Dec12"

STRATEGY_CONTEXT = {
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
    'strategy': {
        'class': StrategyBollingerBands,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 17, 40, 5), 
            OptParam('BB_K', 2, 27, 27, 5), 
            OptParamArray('RulesIndex', [12, 16]), 
            OptParam('MedianPeriod', 5, 5, 15, 5), 
        ],
        'exo_name': 'CL_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
}
