#
#
#  Automatically generated file 
#        Created at: 2016-12-21 12:14:07.963112
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "Bullish_Dec21"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
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
        'exo_name': 'CL_SmartEXO_Ichi_DeltaTargeting_Dec3_Bull_Bull_Spread',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 20, 40, 2), 
            OptParam('BB_K', 2, 22, 42, 4), 
            OptParamArray('RulesIndex', [24, 10]), 
            OptParam('MedianPeriod', 5, 15, 55, 10), 
        ],
        'class': StrategyBollingerBands,
    },
}
