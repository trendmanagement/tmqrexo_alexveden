#
#
#  Automatically generated file 
#        Created at: 2017-01-24 17:27:31.313680
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bullish_Jan17_01"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('ATR period', 1, 7, 15, 1), 
            OptParam('Rolling min max period', 1, 27, 37, 2), 
            OptParamArray('Rules index', [0, 1]), 
        ],
        'exo_name': 'ZN_CallSpread',
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
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
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
}
