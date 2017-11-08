#
#
#  Automatically generated file 
#        Created at: 2017-01-06 11:40:50.112952
#
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = "_Bearish_Dec13"

STRATEGY_CONTEXT = {
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.3),
        'rebalance_time_function': SwarmRebalance.every_friday,
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
            OptParamArray('Direction', [1]), 
            OptParam('conversion_line_period', 9, 20, 22, 1), 
            OptParam('base_line_period', 26, 13, 26, 13), 
            OptParam('leading_spans_lookahead_period', 26, 26, 26, 13), 
            OptParam('leading_span_b_period', 52, 15, 15, 10), 
            OptParamArray('RulesIndex', [13]), 
            OptParam('MedianPeriod', 5, 15, 95, 10), 
        ],
        'class': StrategyIchimokuCloud,
        'exo_name': 'NG_PutSpread',
    },
}
