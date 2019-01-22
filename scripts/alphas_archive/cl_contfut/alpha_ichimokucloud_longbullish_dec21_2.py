#
#
#  Automatically generated file 
#        Created at: 2016-12-21 12:58:51.231690
#
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "Bullish_Dec21_2"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 10, 25, 5), 
            OptParam('base_line_period', 26, 26, 26, 2), 
            OptParam('leading_spans_lookahead_period', 26, 13, 26, 13), 
            OptParam('leading_span_b_period', 52, 15, 55, 10), 
            OptParamArray('RulesIndex', [13]), 
            OptParam('MedianPeriod', 5, 15, 45, 10), 
        ],
        'class': StrategyIchimokuCloud,
        'exo_name': 'CL_ContFut',
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
        'members_count': 1,
    },
}
