#
#
#  Automatically generated file 
#        Created at: 2017-01-25 16:43:51.620964
#
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.strategy import OptParam


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bullish_Jan17_0"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'exo_name': 'ES_PutSpread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('ATR period', 1, 8, 11, 1), 
            OptParam('Rolling min max period', 1, 8, 12, 1), 
            OptParamArray('Rules index', [0]), 
        ],
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
    },
}
