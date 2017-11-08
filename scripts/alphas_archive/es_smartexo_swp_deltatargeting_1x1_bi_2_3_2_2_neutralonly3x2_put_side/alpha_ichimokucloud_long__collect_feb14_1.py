#
#
#  Automatically generated file 
#        Created at: 2017-02-17 11:49:31.027205
#
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "__Collect_Feb14_1"

STRATEGY_CONTEXT = {
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 10, 15, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 13, 13, 13), 
            OptParamArray('RulesIndex', [6, 7, 13, 14]), 
            OptParam('MedianPeriod', 5, 90, 120, 10), 
        ],
        'class': StrategyIchimokuCloud,
        'exo_name': 'ES_SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly3X2_put_side',
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
}
