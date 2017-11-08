#
#
#  Automatically generated file 
#        Created at: 2016-12-13 12:12:00.944996
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bearish_Dec13_2"

STRATEGY_CONTEXT = {
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
    'strategy': {
        'exo_name': 'ZC_PutSpread',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 25, 25, 5), 
            OptParam('base_line_period', 26, 26, 26, 13), 
            OptParam('leading_spans_lookahead_period', 26, 32, 32, 22), 
            OptParam('leading_span_b_period', 52, 16, 16, 8), 
            OptParamArray('RulesIndex', [1]), 
            OptParam('MedianPeriod', 5, 50, 50, 10), 
        ],
        'class': StrategyIchimokuCloud,
    },
}
