from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam, OptParamArray
from backtester.swarms.rankingclasses import *
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_exo import StrategyEXO

STRATEGY_NAME = "EXO"

STRATEGY_SUFFIX = ''

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyEXO,
        'opt_params': [
                        #OptParam(name, default_value, min_value, max_value, step)
                        OptParamArray('Direction', [1]),
            ],
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankingNoRanking(),
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
