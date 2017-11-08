#
#
#  Automatically generated file 
#        Created at: 2016-12-21 12:42:07.961148
#
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "Bearish_Dec21"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 2, 6, 5), 
            OptParam('base_line_period', 26, 13, 26, 13), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 1), 
            OptParam('leading_span_b_period', 52, 10, 20, 5), 
            OptParamArray('RulesIndex', [13]), 
            OptParam('MedianPeriod', 5, 30, 50, 10), 
        ],
        'class': StrategyIchimokuCloud,
        'exo_name': 'CL_SmartEXO_Ichi_DeltaTargeting_Dec3_Bull_Bull_Spread',
    },
}
