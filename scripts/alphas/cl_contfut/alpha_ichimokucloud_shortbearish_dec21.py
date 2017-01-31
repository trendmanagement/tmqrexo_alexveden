#
#
#  Automatically generated file 
#        Created at: 2016-12-21 12:56:19.815801
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "Bearish_Dec21"

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
            OptParam('conversion_line_period', 9, 17, 22, 5), 
            OptParam('base_line_period', 26, 26, 26, 13), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 10), 
            OptParam('leading_span_b_period', 52, 28, 28, 13), 
            OptParamArray('RulesIndex', [7, 13, 0, 14]), 
            OptParam('MedianPeriod', 5, 27, 27, 10), 
        ],
        'exo_name': 'CL_ContFut',
        'class': StrategyIchimokuCloud,
    },
}
