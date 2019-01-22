#
#
#  Automatically generated file 
#        Created at: 2017-02-17 12:09:23.547098
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "__Collect_Feb14_"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 20, 20, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 13, 13, 13), 
            OptParamArray('RulesIndex', [0, 1, 2, 3, 13, 14, 9]), 
            OptParam('MedianPeriod', 5, 105, 125, 20), 
        ],
        'class': StrategyIchimokuCloud,
        'exo_name': 'NG_SmartEXO_SWP_DeltaTargeting_1X1_Bi_2_3_2_2_neutralOnly',
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
}
