#
#
#  Automatically generated file 
#        Created at: 2017-01-16 11:27:22.063978
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bearish_Jan17_2"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'strategy': {
        'class': StrategyIchimokuCloud,
        'exo_name': 'CL_ContFut',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 32, 37, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 28, 28, 13), 
            OptParamArray('RulesIndex', [14]), 
            OptParam('MedianPeriod', 5, 5, 150, 145), 
        ],
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
}
