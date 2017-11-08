#
#
#  Automatically generated file 
#        Created at: 2017-02-14 11:27:13.101442
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.strategy import OptParam


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "__Collect_Feb14_"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'class': StrategyIchimokuCloud,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 7, 7, 1), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 82, 82, 20), 
            OptParamArray('RulesIndex', [11, 0, 1]), 
            OptParam('MedianPeriod', 5, 10, 60, 50), 
        ],
        'exo_name': 'CL_SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly3X2_call_side',
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
