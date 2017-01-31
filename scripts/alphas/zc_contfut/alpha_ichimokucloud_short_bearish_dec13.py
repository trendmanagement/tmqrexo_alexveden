#
#
#  Automatically generated file 
#        Created at: 2016-12-13 12:47:10.416765
#
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bearish_Dec13"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('conversion_line_period', 9, 25, 27, 5), 
            OptParam('base_line_period', 26, 26, 26, 13), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 22), 
            OptParam('leading_span_b_period', 52, 2, 54, 5), 
            OptParamArray('RulesIndex', [11]), 
            OptParam('MedianPeriod', 5, 15, 15, 10), 
        ],
        'exo_name': 'ZC_ContFut',
        'class': StrategyIchimokuCloud,
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
        'members_count': 1,
    },
}
