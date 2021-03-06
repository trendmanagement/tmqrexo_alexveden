from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam, OptParamArray
from backtester.swarms.rankingclasses import *
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud

STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = 'bullish-'

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyIchimokuCloud,
        'exo_name': 'CL_PutSpread',        # <---- Select and paste EXO name from cell above
        'opt_params': [
                        #OptParam(name, default_value, min_value, max_value, step)
                        OptParamArray('Direction', [1]),
                        OptParam('conversion_line_period', 9, 1, 90, 5),
                        OptParam('base_line_period', 26, 13, 13, 13),
                        OptParam('leading_spans_lookahead_period', 26, 26, 26, 13),
                        OptParam('leading_span_b_period', 52, 10, 10, 10),
                        OptParamArray('RulesIndex', np.arange(14)),
                        OptParam('MedianPeriod', 5, 20, 30, 10)
            ],
    },
    'swarm': {
        'members_count': 2,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.8),
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