#
#
#  Automatically generated file 
#        Created at: 2017-01-17 18:07:37.574015
#
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bearish_Jan17"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 7, 7, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 2, 15, 13), 
            OptParamArray('RulesIndex', [6, 14]), 
            OptParam('MedianPeriod', 5, 25, 85, 60), 
        ],
        'class': StrategyIchimokuCloud,
        'exo_name': 'NG_ContFut',
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
}
