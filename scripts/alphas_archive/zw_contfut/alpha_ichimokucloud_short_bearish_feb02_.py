#
#
#  Automatically generated file 
#        Created at: 2017-02-09 10:11:28.530560
#
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bearish_Feb02_"

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
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 23, 23, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 2, 58, 13), 
            OptParam('leading_span_b_period', 52, 15, 15, 15), 
            OptParamArray('RulesIndex', [1, 13]), 
            OptParam('MedianPeriod', 5, 14, 26, 12), 
        ],
        'exo_name': 'ZW_ContFut',
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
}
