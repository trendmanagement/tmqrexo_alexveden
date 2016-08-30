from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam, OptParamArray
from backtester.swarms.rankingclasses import *
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_renko_no_exit_on_patterns import StrategyRenkoPatterns_no_exit_on_patterns

STRATEGY_NAME = "Renko"

STRATEGY_SUFFIX = ''

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyRenkoPatterns_no_exit_on_patterns,
        'exo_name': 'strategy_340240',
        'opt_params': [
            # OptParam(name, default_value, min_value, max_value, step)
            OptParamArray('Direction', [1]),
            OptParam('BoxSize', 500, 100, 1000, 50),
            OptParam('MoveCount', 2, 2, 2, 1),
            OptParamArray('RulesIndex', np.arange(9)),
            OptParam('MedianPeriod', 5, 1, 20, 2)

        ],
    },
    'swarm': {
        'members_count': 5,
        'ranking_class': RankerHighestReturns(return_period=14),
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