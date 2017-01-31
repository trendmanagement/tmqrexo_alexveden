#
#
#  Automatically generated file 
#        Created at: 2016-12-12 11:31:38.399196
#
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bearish_Dec12"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 15, 15, 2), 
            OptParam('base_line_period', 26, 13, 13, 13), 
            OptParam('leading_spans_lookahead_period', 26, 13, 54, 13), 
            OptParam('leading_span_b_period', 52, 26, 26, 2), 
            OptParamArray('RulesIndex', [11]), 
            OptParam('MedianPeriod', 5, 50, 50, 2), 
        ],
        'exo_name': 'CL_SmartEXO_Ichi_Bearish_Straddle_150Delta',
        'class': StrategyIchimokuCloud,
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
}
