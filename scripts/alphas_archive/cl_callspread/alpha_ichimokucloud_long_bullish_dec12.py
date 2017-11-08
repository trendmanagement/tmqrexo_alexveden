#
#
#  Automatically generated file 
#        Created at: 2016-12-12 11:04:32.872872
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bullish_Dec12"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 14, 20, 6), 
            OptParam('base_line_period', 26, 26, 26, 13), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 6, 26, 2), 
            OptParamArray('RulesIndex', [6, 13]), 
            OptParam('MedianPeriod', 5, 25, 35, 10), 
        ],
        'class': StrategyIchimokuCloud,
        'exo_name': 'CL_CallSpread',
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 2,
    },
}
