from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam, OptParamArray
from backtester.swarms.rankingclasses import *
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_renko_no_exit_on_patterns import StrategyRenkoPatterns_no_exit_on_patterns

STRATEGY_NAME = StrategyRenkoPatterns_no_exit_on_patterns.name

STRATEGY_SUFFIX = 'bullish-'

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyRenkoPatterns_no_exit_on_patterns,
        'exo_name': 'CL_PutSpread',  # <---- Select and paste EXO name from cell above
        'opt_params': [
            # OptParam(name, default_value, min_value, max_value, step)
            OptParamArray('Direction', [1]),
            OptParam('BoxSize', 500, 400, 500, 100),
            OptParam('MoveCount', 2, 3, 3, 1),
            OptParamArray('RulesIndex', np.arange(9)),
            OptParam('MedianPeriod', 5, 20, 20, 19)

        ],
    },
    'swarm': {
        'members_count': 2,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
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