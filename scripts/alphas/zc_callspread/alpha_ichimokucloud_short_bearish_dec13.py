#
#
#  Automatically generated file 
#        Created at: 2016-12-13 12:39:22.996215
#
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bearish_Dec13"

STRATEGY_CONTEXT = {
    'strategy': {
        'exo_name': 'ZC_CallSpread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 2, 15, 13), 
            OptParam('base_line_period', 26, 26, 26, 13), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 1), 
            OptParam('leading_span_b_period', 52, 13, 35, 11), 
            OptParamArray('RulesIndex', [13]), 
            OptParam('MedianPeriod', 5, 13, 13, 13), 
        ],
        'class': StrategyIchimokuCloud,
    },
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
