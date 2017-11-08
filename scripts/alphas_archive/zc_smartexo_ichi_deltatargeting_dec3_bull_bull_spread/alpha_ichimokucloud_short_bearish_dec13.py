#
#
#  Automatically generated file 
#        Created at: 2016-12-13 12:25:58.782533
#
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bearish_Dec13"

STRATEGY_CONTEXT = {
    'strategy': {
        'exo_name': 'ZC_SmartEXO_Ichi_DeltaTargeting_Dec3_Bull_Bull_Spread',
        'class': StrategyIchimokuCloud,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 2, 2, 5), 
            OptParam('base_line_period', 26, 26, 26, 13), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 1), 
            OptParam('leading_span_b_period', 52, 25, 25, 10), 
            OptParamArray('RulesIndex', [13, 0]), 
            OptParam('MedianPeriod', 5, 30, 90, 20), 
        ],
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
}
