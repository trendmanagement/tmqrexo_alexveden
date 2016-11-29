from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam, OptParamArray
from backtester.swarms.rankingclasses import *
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_bbands import StrategyBollingerBands

STRATEGY_NAME = "IchimokuCloud"

STRATEGY_SUFFIX = 'custom-cl-smartexo-alpha'

STRATEGY_CONTEXT = {
   'strategy': {
       'class': StrategyBollingerBands,
       'exo_name': 'SmartEXO_Ichi_Bullish_Straddle_150Delta_ExpHedged_Nov22_2016', # <---- Select and paste EXO name from cell above
       'opt_params': [
                       #OptParam(name, default_value, min_value, max_value, step)
                       OptParamArray('Direction', [1]),
                       OptParam('BB_Period', 20, 15, 15, 5),
                       OptParam('BB_K', 2, 15, 35, 5),
                       ### All rules
                       OptParamArray('RulesIndex', [0,3]),
                       OptParam('MedianPeriod', 5, 35, 95, 20)
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