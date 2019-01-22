from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam, OptParamArray
from backtester.swarms.rankingclasses import *
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_macross_with_trail import StrategyMACrossTrail

STRATEGY_NAME = StrategyMACrossTrail.name

STRATEGY_SUFFIX = 'bearish-'

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyMACrossTrail,
        'exo_name': 'ZW_PutSpread',        # <---- Select and paste EXO name from cell above
        'opt_params': [
                #OptParam(name, default_value, min_value, max_value, step)
                OptParamArray('Direction', [1]),
                OptParam('SlowMAPeriod', 20, 10, 110, 50),
                OptParam('FastMAPeriod', 2, 2, 2, 5),
                OptParam('MedianPeriod', 5, 45, 45, 1)
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