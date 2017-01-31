#
#
#  Automatically generated file 
#        Created at: 2017-01-22 12:49:36.661565
#
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bi_Jan17_0s"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
        'exo_name': 'ZC_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('ATR period', 1, 2, 6, 1), 
            OptParam('Rolling min max period', 1, 75, 190, 5), 
            OptParamArray('Rules index', [0]), 
        ],
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
