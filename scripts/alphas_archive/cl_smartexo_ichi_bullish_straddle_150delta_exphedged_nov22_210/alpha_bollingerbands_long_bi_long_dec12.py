#
#
#  Automatically generated file 
#        Created at: 2016-12-12 12:10:36.359288
#
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParam


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bi_Long_Dec12"

STRATEGY_CONTEXT = {
    'strategy': {
        'exo_name': 'CL_SmartEXO_Ichi_Bullish_Straddle_150Delta_ExpHedged_Nov22_210',
        'class': StrategyBollingerBands,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 15, 15, 5), 
            OptParam('BB_K', 2, 15, 35, 5), 
            OptParamArray('RulesIndex', [0, 3]), 
            OptParam('MedianPeriod', 5, 35, 95, 20), 
        ],
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
}
