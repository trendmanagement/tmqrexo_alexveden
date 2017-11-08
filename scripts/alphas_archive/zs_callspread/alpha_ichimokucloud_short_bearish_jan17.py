#
#
#  Automatically generated file 
#        Created at: 2017-01-17 11:43:30.752402
#
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bearish_Jan17"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'strategy': {
        'class': StrategyIchimokuCloud,
        'exo_name': 'ZS_CallSpread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 37, 57, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 28, 54, 13), 
            OptParamArray('RulesIndex', [3, 4, 6, 5, 7]), 
            OptParam('MedianPeriod', 5, 45, 45, 10), 
        ],
    },
}
