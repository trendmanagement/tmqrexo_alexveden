#
#
#  Automatically generated file 
#        Created at: 2016-12-14 12:13:47.187236
#
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bullish_Dec13"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyIchimokuCloud,
        'exo_name': 'NG_PutSpread',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 12, 25, 12), 
            OptParam('base_line_period', 26, 26, 72, 13), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 35, 55, 10), 
            OptParamArray('RulesIndex', [13]), 
            OptParam('MedianPeriod', 5, 15, 95, 10), 
        ],
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
}
