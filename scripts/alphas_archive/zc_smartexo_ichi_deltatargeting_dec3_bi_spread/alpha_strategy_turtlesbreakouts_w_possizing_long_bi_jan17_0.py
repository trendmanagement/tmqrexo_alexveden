#
#
#  Automatically generated file 
#        Created at: 2017-01-22 12:47:23.323673
#
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bi_Jan17_0"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('ATR period', 1, 3, 14, 11), 
            OptParam('Rolling min max period', 1, 6, 24, 18), 
            OptParamArray('Rules index', [0]), 
        ],
        'exo_name': 'ZC_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
    },
}
