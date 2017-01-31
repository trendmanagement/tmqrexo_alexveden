#
#
#  Automatically generated file 
#        Created at: 2016-12-21 12:19:15.928533
#
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray
from strategies.strategy_bbands import StrategyBollingerBands


STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = "Bullish_Dec21"

STRATEGY_CONTEXT = {
    'strategy': {
        'exo_name': 'CL_ContFut',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParamArray('BB_Period', [20, 60]), 
            OptParamArray('BB_K', [5, 5]), 
            OptParamArray('RulesIndex', [9, 13]), 
            OptParam('MedianPeriod', 5, 6, 6, 10), 
        ],
        'class': StrategyBollingerBands,
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
}
