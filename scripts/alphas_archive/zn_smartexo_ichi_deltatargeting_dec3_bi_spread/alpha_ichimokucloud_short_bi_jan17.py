#
#
#  Automatically generated file 
#        Created at: 2017-01-24 17:13:38.004612
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bi_Jan17"

STRATEGY_CONTEXT = {
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 27, 62, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 9, 9, 13), 
            OptParamArray('RulesIndex', [14, 13, 7]), 
            OptParam('MedianPeriod', 5, 25, 65, 10), 
        ],
        'exo_name': 'ZN_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'class': StrategyIchimokuCloud,
    },
}
