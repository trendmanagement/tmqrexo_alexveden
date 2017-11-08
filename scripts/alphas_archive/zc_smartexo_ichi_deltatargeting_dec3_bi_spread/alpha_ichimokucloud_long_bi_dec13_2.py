#
#
#  Automatically generated file 
#        Created at: 2016-12-21 10:51:46.021007
#
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bi_Dec13_2"

STRATEGY_CONTEXT = {
    'strategy': {
        'exo_name': 'ZC_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 18, 18, 2), 
            OptParam('base_line_period', 26, 26, 26, 13), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 2), 
            OptParam('leading_span_b_period', 52, 32, 32, 10), 
            OptParamArray('RulesIndex', [13]), 
            OptParam('MedianPeriod', 5, 13, 65, 13), 
        ],
        'class': StrategyIchimokuCloud,
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
}
