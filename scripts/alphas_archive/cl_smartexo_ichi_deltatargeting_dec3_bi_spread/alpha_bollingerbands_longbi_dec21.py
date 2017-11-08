#
#
#  Automatically generated file 
#        Created at: 2016-12-21 12:11:09.199070
#
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParamArray
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "Bi_Dec21"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 17, 40, 5), 
            OptParam('BB_K', 2, 27, 27, 5), 
            OptParamArray('RulesIndex', [12, 16]), 
            OptParam('MedianPeriod', 5, 5, 15, 5), 
        ],
        'class': StrategyBollingerBands,
        'exo_name': 'CL_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
}
