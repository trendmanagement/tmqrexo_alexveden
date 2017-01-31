#
#
#  Automatically generated file 
#        Created at: 2017-01-17 18:13:38.754176
#
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bullish_Jan17"

STRATEGY_CONTEXT = {
    'strategy': {
        'exo_name': 'NG_PutSpread',
        'class': StrategyIchimokuCloud,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 7, 37, 5), 
            OptParam('base_line_period', 26, 13, 13, 2), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 2, 15, 13), 
            OptParamArray('RulesIndex', [7, 10, 6]), 
            OptParam('MedianPeriod', 5, 25, 85, 60), 
        ],
    },
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
}
