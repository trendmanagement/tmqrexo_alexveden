#
#
#  Automatically generated file 
#        Created at: 2017-02-18 16:42:06.848146
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Collect_Feb14_"

STRATEGY_CONTEXT = {
    'strategy': {
        'exo_name': 'ZW_SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 2, 14, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 13, 13, 13), 
            OptParamArray('RulesIndex', [14]), 
            OptParam('MedianPeriod', 5, 105, 220, 20), 
        ],
        'class': StrategyIchimokuCloud,
    },
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
}
