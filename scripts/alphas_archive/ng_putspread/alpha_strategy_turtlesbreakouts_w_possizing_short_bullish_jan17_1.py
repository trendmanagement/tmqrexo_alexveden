#
#
#  Automatically generated file 
#        Created at: 2017-01-23 12:00:49.732007
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bullish_Jan17_1"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
        'members_count': 1,
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('ATR period', 1, 6, 10, 1), 
            OptParam('Rolling min max period', 1, 30, 90, 2), 
            OptParamArray('Rules index', [1]), 
        ],
        'exo_name': 'NG_PutSpread',
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
    },
}
