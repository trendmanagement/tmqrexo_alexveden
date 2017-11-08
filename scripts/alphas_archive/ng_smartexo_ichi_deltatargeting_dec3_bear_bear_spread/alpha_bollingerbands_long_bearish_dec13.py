#
#
#  Automatically generated file 
#        Created at: 2016-12-14 11:37:33.877893
#
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_bbands import StrategyBollingerBands
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "_Bearish_Dec13"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('BB_Period', 20, 32, 32, 10), 
            OptParam('BB_K', 2, 82, 82, 10), 
            OptParamArray('RulesIndex', [1]), 
            OptParam('MedianPeriod', 5, 13, 13, 13), 
        ],
        'class': StrategyBollingerBands,
        'exo_name': 'NG_SmartEXO_Ichi_DeltaTargeting_Dec3_Bear_Bear_Spread',
    },
}
