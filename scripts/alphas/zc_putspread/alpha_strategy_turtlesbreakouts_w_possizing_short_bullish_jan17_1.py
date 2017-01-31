#
#
#  Automatically generated file 
#        Created at: 2017-01-22 12:44:42.501034
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.strategy import OptParamArray


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bullish_Jan17_1"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'exo_name': 'ZC_PutSpread',
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('ATR period', 1, 2, 14, 1), 
            OptParam('Rolling min max period', 1, 2, 50, 5), 
            OptParamArray('Rules index', [1]), 
        ],
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
    },
}
