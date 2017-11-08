#
#
#  Automatically generated file 
#        Created at: 2017-01-19 16:28:05.161339
#
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bi_Jan17"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
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
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 42, 54, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 2, 2, 13), 
            OptParamArray('RulesIndex', [6, 7]), 
            OptParam('MedianPeriod', 5, 14, 26, 2), 
        ],
        'exo_name': 'NG_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
    },
}
