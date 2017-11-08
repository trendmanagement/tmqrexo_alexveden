#
#
#  Automatically generated file 
#        Created at: 2017-02-08 10:36:23.209561
#
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bullish_0_1_Feb02_"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('ATR period', 1, 2, 8, 2), 
            OptParam('Rolling min max period', 1, 30, 50, 2), 
            OptParamArray('Rules index', [0]), 
        ],
        'exo_name': 'ZS_ContFut',
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
