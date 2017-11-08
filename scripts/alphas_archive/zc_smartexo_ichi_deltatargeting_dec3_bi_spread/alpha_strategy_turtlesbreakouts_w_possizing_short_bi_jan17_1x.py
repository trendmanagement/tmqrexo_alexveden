#
#
#  Automatically generated file 
#        Created at: 2017-01-22 12:52:20.491402
#
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bi_Jan17_1X"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
        'members_count': 1,
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'strategy': {
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('ATR period', 1, 5, 8, 1), 
            OptParam('Rolling min max period', 1, 75, 160, 5), 
            OptParamArray('Rules index', [1]), 
        ],
        'exo_name': 'ZC_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
    },
}
