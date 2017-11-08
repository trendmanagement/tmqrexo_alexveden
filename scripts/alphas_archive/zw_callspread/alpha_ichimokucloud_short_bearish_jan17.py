#
#
#  Automatically generated file 
#        Created at: 2017-01-25 12:12:53.548975
#
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bearish_Jan17"

STRATEGY_CONTEXT = {
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
    'strategy': {
        'class': StrategyIchimokuCloud,
        'exo_name': 'ZW_CallSpread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 53, 53, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 2, 58, 13), 
            OptParam('leading_span_b_period', 52, 2, 39, 15), 
            OptParamArray('RulesIndex', [1, 7]), 
            OptParam('MedianPeriod', 5, 14, 26, 12), 
        ],
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
