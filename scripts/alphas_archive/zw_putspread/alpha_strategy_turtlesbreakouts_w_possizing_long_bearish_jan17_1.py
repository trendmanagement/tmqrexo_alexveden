#
#
#  Automatically generated file 
#        Created at: 2017-01-25 12:38:16.268446
#
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bearish_Jan17_1"

STRATEGY_CONTEXT = {
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
        'exo_name': 'ZW_PutSpread',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('ATR period', 1, 9, 15, 1), 
            OptParam('Rolling min max period', 1, 2, 2, 1), 
            OptParamArray('Rules index', [1]), 
        ],
    },
}
