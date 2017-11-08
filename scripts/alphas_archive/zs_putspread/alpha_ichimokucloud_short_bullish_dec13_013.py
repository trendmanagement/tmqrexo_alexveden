#
#
#  Automatically generated file 
#        Created at: 2016-12-16 11:28:34.275501
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bullish_Dec13_013"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 15, 25, 13), 
            OptParam('base_line_period', 26, 26, 26, 13), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 10), 
            OptParam('leading_span_b_period', 52, 13, 54, 10), 
            OptParamArray('RulesIndex', [2, 13]), 
            OptParam('MedianPeriod', 5, 45, 55, 10), 
        ],
        'class': StrategyIchimokuCloud,
        'exo_name': 'ZS_PutSpread',
    },
}
