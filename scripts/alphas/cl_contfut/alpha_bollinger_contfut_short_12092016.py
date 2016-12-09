from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam, OptParamArray
from backtester.swarms.rankingclasses import *
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_bbands import StrategyBollingerBands

STRATEGY_NAME = StrategyBollingerBands.name

STRATEGY_SUFFIX = 'bollinger-short-12092016'

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyBollingerBands,
        'exo_name': 'CL_ContFut',  # <---- Select and paste EXO name from cell above
        'opt_params': [
            # OptParam(name, default_value, min_value, max_value, step)
            OptParamArray('Direction', [-1]),
            OptParam('BB_Period', 20, 4, 15, 1),
            OptParam('BB_K', 2, 27, 57, 10),

            # OptParamArray('RulesIndex', np.arange(26)),
            ### Trend 0:5
            # OptParamArray('RulesIndex', np.arange(26)[1:2]),

            ### Vola breakout 5:10
            # OptParamArray('RulesIndex', np.arange(26)[5:10]),

            ### High vola(BBands width percent rank > 80-90) 10:15
            # OptParamArray('RulesIndex', np.arange(26)[10:11]),

            ### %B rules 15:26
            # OptParamArray('RulesIndex', np.arange(26)[15:26]),

            ### All rules
            OptParamArray('RulesIndex', [3]),
            # OptParamArray('RulesIndex', np.arange(26)[0:26]),

            OptParam('MedianPeriod', 5, 25, 25, 10)
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