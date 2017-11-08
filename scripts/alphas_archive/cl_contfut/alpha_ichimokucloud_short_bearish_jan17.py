#
#
#  Automatically generated file 
#        Created at: 2017-01-16 10:42:36.950151
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bearish_Jan17"

STRATEGY_CONTEXT = {
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'class': StrategyIchimokuCloud,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 32, 37, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 28, 28, 13), 
            OptParamArray('RulesIndex', [14]), 
            OptParam('MedianPeriod', 5, 5, 15, 10), 
        ],
        'exo_name': 'CL_ContFut',
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
}
