#
#
#  Automatically generated file 
#        Created at: 2017-01-24 17:43:09.080285
#
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bullish_Jan17_1"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
        'exo_name': 'ZN_PutSpread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('ATR period', 1, 5, 5, 1), 
            OptParam('Rolling min max period', 1, 11, 31, 2), 
            OptParamArray('Rules index', [1]), 
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
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
