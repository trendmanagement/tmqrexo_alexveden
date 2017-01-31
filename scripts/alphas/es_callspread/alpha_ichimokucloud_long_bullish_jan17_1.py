#
#
#  Automatically generated file 
#        Created at: 2017-01-25 19:55:24.834575
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyIchimokuCloud.name

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
        'class': StrategyIchimokuCloud,
        'exo_name': 'ES_CallSpread',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 50, 50, 15), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 28, 28, 13), 
            OptParamArray('RulesIndex', [11, 0, 1, 14, 13]), 
            OptParam('MedianPeriod', 5, 20, 20, 2), 
        ],
    },
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
}
