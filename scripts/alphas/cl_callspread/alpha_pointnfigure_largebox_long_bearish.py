from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam, OptParamArray
from backtester.swarms.rankingclasses import *
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_pnf import StrategyPointAndFigurePatterns

STRATEGY_NAME = "PointAndFigure"

STRATEGY_SUFFIX = 'largebox-bearish-'

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyPointAndFigurePatterns,
        'exo_name': 'CL_CallSpread',        # <---- Select and paste EXO name from cell above
        'opt_params': [
                        #OptParam(name, default_value, min_value, max_value, step)
                        OptParamArray('Direction', [1]),
                        OptParam('BoxSize', 1, 300, 1000, 100),
                        OptParam('Reversal', 2, 2, 3, 1),
                        OptParamArray('MaxMinWindowPercent', [0.05]),
                        OptParam('ColumnConsecMoveCount', 2, 1, 1, 1),
                        OptParamArray('RulesIndex', np.arange(9)),
                        OptParam('MedianPeriod', 5, 30, 50, 10),

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