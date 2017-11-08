#
#
#  Automatically generated file 
#        Created at: 2016-12-21 14:37:29.618781
#
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bi_Dec13"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyIchimokuCloud,
        'exo_name': 'ZS_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 41, 41, 13), 
            OptParam('base_line_period', 26, 26, 26, 13), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 10), 
            OptParam('leading_span_b_period', 52, 28, 54, 13), 
            OptParamArray('RulesIndex', [13, 1, 3]), 
            OptParam('MedianPeriod', 5, 55, 75, 10), 
        ],
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
}
