#
#
#  Automatically generated file 
#        Created at: 2017-01-19 22:10:04.069561
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bearish_Jan17"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 2, 28, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 2, 54, 13), 
            OptParamArray('RulesIndex', [13, 7, 14, 0]), 
            OptParam('MedianPeriod', 5, 2, 47, 10), 
        ],
        'class': StrategyIchimokuCloud,
        'exo_name': 'ZC_ContFut',
    },
}
