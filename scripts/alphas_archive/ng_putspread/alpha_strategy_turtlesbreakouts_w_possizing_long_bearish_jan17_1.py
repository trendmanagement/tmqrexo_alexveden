#
#
#  Automatically generated file 
#        Created at: 2017-01-23 11:58:43.899660
#
from backtester.strategy import OptParamArray
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bearish_Jan17_1"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
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
            OptParamArray('Direction', [1]), 
            OptParam('ATR period', 1, 7, 10, 1), 
            OptParam('Rolling min max period', 1, 17, 22, 2), 
            OptParamArray('Rules index', [1]), 
        ],
        'exo_name': 'NG_PutSpread',
    },
}
