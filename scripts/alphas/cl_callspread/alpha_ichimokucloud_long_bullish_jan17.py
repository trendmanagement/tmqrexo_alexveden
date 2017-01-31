#
#
#  Automatically generated file 
#        Created at: 2017-01-16 10:11:14.472828
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bullish_Jan17"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'exo_name': 'CL_CallSpread',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 17, 28, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 15, 54, 13), 
            OptParamArray('RulesIndex', [13, 7, 14]), 
            OptParam('MedianPeriod', 5, 2, 47, 10), 
        ],
        'class': StrategyIchimokuCloud,
    },
}
