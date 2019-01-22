#
#
#  Automatically generated file 
#        Created at: 2017-01-24 17:49:12.110711
#
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bi_Jan17_1"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('ATR period', 1, 5, 12, 1), 
            OptParam('Rolling min max period', 1, 76, 172, 10), 
            OptParamArray('Rules index', [1]), 
        ],
        'exo_name': 'ZN_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
    },
}
