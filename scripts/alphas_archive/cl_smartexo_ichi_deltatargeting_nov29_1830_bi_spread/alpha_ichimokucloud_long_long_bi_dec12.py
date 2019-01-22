#
#
#  Automatically generated file 
#        Created at: 2016-12-12 11:36:59.173772
#
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Long_Bi_Dec12"

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
            OptParam('conversion_line_period', 9, 20, 20, 2), 
            OptParam('base_line_period', 26, 26, 26, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 5, 55, 10), 
            OptParamArray('RulesIndex', [10, 13]), 
            OptParam('MedianPeriod', 5, 25, 25, 10), 
        ],
        'exo_name': 'CL_SmartEXO_Ichi_DeltaTargeting_Nov29_1830_Bi_Spread',
        'class': StrategyIchimokuCloud,
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
}
