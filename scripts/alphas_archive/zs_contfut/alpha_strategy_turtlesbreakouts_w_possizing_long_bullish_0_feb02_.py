#
#
#  Automatically generated file 
#        Created at: 2017-02-08 10:29:06.886935
#
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bullish_0_Feb02_"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('ATR period', 1, 24, 24, 2), 
            OptParam('Rolling min max period', 1, 95, 125, 10), 
            OptParamArray('Rules index', [0]), 
        ],
        'exo_name': 'ZS_ContFut',
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
