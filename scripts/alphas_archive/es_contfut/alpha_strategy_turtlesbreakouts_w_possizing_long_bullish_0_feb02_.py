#
#
#  Automatically generated file 
#        Created at: 2017-02-08 12:44:52.191463
#
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bullish_0_Feb02_"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('ATR period', 1, 15, 25, 5), 
            OptParam('Rolling min max period', 1, 15, 20, 1), 
            OptParamArray('Rules index', [0]), 
        ],
        'exo_name': 'ES_ContFut',
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
    },
}
