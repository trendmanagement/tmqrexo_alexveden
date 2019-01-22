#
#
#  Automatically generated file 
#        Created at: 2016-12-14 11:46:56.415371
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bi_Dec13"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
    },
    'strategy': {
        'exo_name': 'NG_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'class': StrategyIchimokuCloud,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 27, 27, 5), 
            OptParam('base_line_period', 26, 13, 13, 13), 
            OptParam('leading_spans_lookahead_period', 26, 1, 54, 13), 
            OptParam('leading_span_b_period', 52, 5, 5, 10), 
            OptParamArray('RulesIndex', [13, 5]), 
            OptParam('MedianPeriod', 5, 20, 20, 10), 
        ],
    },
}
