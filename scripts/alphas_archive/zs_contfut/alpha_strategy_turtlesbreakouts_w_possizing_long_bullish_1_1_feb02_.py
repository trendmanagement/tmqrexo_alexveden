#
#
#  Automatically generated file 
#        Created at: 2017-02-08 10:38:09.107727
#
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bullish_1_1_Feb02_"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
        'exo_name': 'ZS_ContFut',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('ATR period', 1, 2, 8, 2), 
            OptParam('Rolling min max period', 1, 2, 50, 2), 
            OptParamArray('Rules index', [1]), 
        ],
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
