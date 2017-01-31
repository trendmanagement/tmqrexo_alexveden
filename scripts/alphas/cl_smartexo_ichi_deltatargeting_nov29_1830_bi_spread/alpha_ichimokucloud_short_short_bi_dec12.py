#
#
#  Automatically generated file 
#        Created at: 2016-12-12 11:18:54.591659
#
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Short_Bi_Dec12"

STRATEGY_CONTEXT = {
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 4, 4, 2), 
            OptParam('base_line_period', 26, 26, 26, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 35, 35, 10), 
            OptParamArray('RulesIndex', [7, 9]), 
            OptParam('MedianPeriod', 5, 15, 15, 10), 
        ],
        'class': StrategyIchimokuCloud,
        'exo_name': 'CL_SmartEXO_Ichi_DeltaTargeting_Nov29_1830_Bi_Spread',
    },
}
