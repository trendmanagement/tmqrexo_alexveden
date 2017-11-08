#
#
#  Automatically generated file 
#        Created at: 2017-02-08 11:58:04.289208
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bearish_0_Feb02_"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('ATR period', 1, 2, 20, 5), 
            OptParam('Rolling min max period', 1, 14, 20, 2), 
            OptParamArray('Rules index', [0]), 
        ],
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
        'exo_name': 'CL_ContFut',
    },
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
}
