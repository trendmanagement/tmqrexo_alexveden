#
#
#  Automatically generated file 
#        Created at: 2016-12-12 10:30:46.829767
#
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_macross_with_trail import StrategyMACrossTrail
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam


STRATEGY_NAME = StrategyMACrossTrail.name

STRATEGY_SUFFIX = "-test"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'swarm': {
        'members_count': 2,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.75),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'class': StrategyMACrossTrail,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('SlowMAPeriod', 20, 50, 70, 10), 
            OptParam('FastMAPeriod', 2, 5, 5, 5), 
            OptParam('MedianPeriod', 5, 20, 20, 1), 
        ],
        'exo_name': 'ES_PutSpread',
        'direction': -1,
    },
}
