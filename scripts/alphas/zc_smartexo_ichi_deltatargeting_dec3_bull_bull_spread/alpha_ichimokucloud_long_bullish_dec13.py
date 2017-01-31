#
#
#  Automatically generated file 
#        Created at: 2016-12-13 12:24:09.201000
#
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bullish_Dec13"

STRATEGY_CONTEXT = {
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 12, 12, 5), 
            OptParam('base_line_period', 26, 13, 13, 13), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 1), 
            OptParam('leading_span_b_period', 52, 5, 5, 10), 
            OptParamArray('RulesIndex', [13, 10]), 
            OptParam('MedianPeriod', 5, 30, 30, 20), 
        ],
        'exo_name': 'ZC_SmartEXO_Ichi_DeltaTargeting_Dec3_Bull_Bull_Spread',
        'class': StrategyIchimokuCloud,
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
