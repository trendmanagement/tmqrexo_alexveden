#
#
#  Automatically generated file 
#        Created at: 2017-01-22 12:28:57.869712
#
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bi_Jan17"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'exo_name': 'ZC_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 2, 42, 40), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 9, 9, 13), 
            OptParamArray('RulesIndex', [13, 14]), 
            OptParam('MedianPeriod', 5, 15, 30, 5), 
        ],
        'class': StrategyIchimokuCloud,
    },
}
