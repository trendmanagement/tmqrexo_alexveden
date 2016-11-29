from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam, OptParamArray
from backtester.swarms.rankingclasses import *
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud

STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = 'bearish-'

STRATEGY_CONTEXT = {
    'strategy': {
       'class': StrategyIchimokuCloud,
       'exo_name': 'ZC_PutSpread',        # <---- Select and paste EXO name from cell above
       #'exo_storage': storage,
       'opt_params': [
                       #OptParam(name, default_value, min_value, max_value, step)
                       OptParamArray('Direction', [1]),
                       OptParam('conversion_line_period', 9, 25, 25, 5),
                       OptParam('base_line_period', 26, 26, 26, 13),
                       OptParam('leading_spans_lookahead_period', 26, 2, 54, 2),
                       OptParam('leading_span_b_period', 52, 20, 20, 2),
                       OptParamArray('RulesIndex', [1]),
                       OptParam('MedianPeriod', 5, 50, 50, 10)
           ],
   },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        }
    }
}

