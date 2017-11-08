#
#
#  Automatically generated file 
#        Created at: 2016-12-16 11:17:40.443940
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bearish_Dec13"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyIchimokuCloud,
        'exo_name': 'ZS_CallSpread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 31, 31, 13), 
            OptParam('base_line_period', 26, 26, 26, 13), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 10), 
            OptParam('leading_span_b_period', 52, 39, 39, 13), 
            OptParamArray('RulesIndex', [13, 10]), 
            OptParam('MedianPeriod', 5, 15, 45, 10), 
        ],
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
}
