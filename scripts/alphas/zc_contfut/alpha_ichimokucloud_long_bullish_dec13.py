#
#
#  Automatically generated file 
#        Created at: 2016-12-13 12:43:44.646520
#
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bullish_Dec13"

STRATEGY_CONTEXT = {
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'class': StrategyIchimokuCloud,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 22, 22, 5), 
            OptParam('base_line_period', 26, 26, 26, 13), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 22), 
            OptParam('leading_span_b_period', 52, 7, 7, 5), 
            OptParamArray('RulesIndex', [10, 13]), 
            OptParam('MedianPeriod', 5, 25, 25, 10), 
        ],
        'exo_name': 'ZC_ContFut',
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
