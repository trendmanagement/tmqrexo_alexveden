from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam, OptParamArray
from backtester.swarms.rankingclasses import *
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_pnf import StrategyPointAndFigurePatterns

STRATEGY_NAME = "IchimokuCloud"

STRATEGY_SUFFIX = 'custom-cl-smartexo-alpha'

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyIchimokuCloud,
        'exo_name': 'CL_SmartEXO_Ichi_Bearish_Straddle_150Delta',        # <---- Select and paste EXO name from cell above
        'exo_storage': storage,
        'opt_params': [
                        #OptParam(name, default_value, min_value, max_value, step)
                        OptParamArray('Direction', [1]),
                        OptParam('conversion_line_period', 9, 15, 15, 1),
                        OptParam('base_line_period', 26, 13, 13, 13),
                        OptParam('leading_spans_lookahead_period', 26, 13, 54, 13),
                        OptParam('leading_span_b_period', 52, 26, 26, 2),
                        #OptParamArray('RulesIndex', np.arange(14)),
                        OptParamArray('RulesIndex', [11]),
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