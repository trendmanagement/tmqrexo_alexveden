#
#
#  Automatically generated file 
#        Created at: 2017-01-19 15:57:40.112501
#
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bi_Jan17"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'exo_name': 'NG_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 12, 12, 10), 
            OptParam('BB_K', 2, 2, 60, 10), 
            OptParamArray('RulesIndex', [20]), 
            OptParam('MedianPeriod', 5, 7, 7, 10), 
        ],
        'class': StrategyBollingerBands,
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
