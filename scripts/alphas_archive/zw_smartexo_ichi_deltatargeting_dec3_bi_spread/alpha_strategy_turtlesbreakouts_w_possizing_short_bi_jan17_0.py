#
#
#  Automatically generated file 
#        Created at: 2017-01-25 12:47:11.279444
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bi_Jan17_0"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('ATR period', 1, 7, 13, 1), 
            OptParam('Rolling min max period', 1, 20, 22, 2), 
            OptParamArray('Rules index', [0]), 
        ],
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
        'exo_name': 'ZW_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
}
