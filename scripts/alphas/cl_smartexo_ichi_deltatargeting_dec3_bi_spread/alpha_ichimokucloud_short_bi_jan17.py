#
#
#  Automatically generated file 
#        Created at: 2017-01-17 09:49:08.347317
#
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bi_Jan17"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyIchimokuCloud,
        'exo_name': 'CL_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 17, 30, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 54, 54, 13), 
            OptParamArray('RulesIndex', [7]), 
            OptParam('MedianPeriod', 5, 55, 125, 10), 
        ],
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
