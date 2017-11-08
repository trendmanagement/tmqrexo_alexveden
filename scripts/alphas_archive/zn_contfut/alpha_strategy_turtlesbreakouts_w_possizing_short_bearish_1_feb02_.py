#
#
#  Automatically generated file 
#        Created at: 2017-02-08 17:40:57.812558
#
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bearish_1_Feb02_"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'strategy': {
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('ATR period', 1, 10, 10, 2), 
            OptParam('Rolling min max period', 1, 17, 20, 1), 
            OptParamArray('Rules index', [1]), 
        ],
        'exo_name': 'ZN_ContFut',
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
}
