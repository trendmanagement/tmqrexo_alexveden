#
#
#  Automatically generated file 
#        Created at: 2017-01-24 17:33:03.054141
#
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bearish_Jan17"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
    },
    'strategy': {
        'exo_name': 'ZN_CallSpread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('ATR period', 1, 5, 5, 1), 
            OptParam('Rolling min max period', 1, 19, 19, 10), 
            OptParamArray('Rules index', [1]), 
        ],
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
    },
}
