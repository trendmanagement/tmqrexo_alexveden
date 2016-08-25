from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam, OptParamArray
from backtester.swarms.rankingclasses import *
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_pnf import StrategyPointAndFigurePatterns

STRATEGY_NAME = "PointAndFigure"

STRATEGY_SUFFIX = ''

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyPointAndFigurePatterns,
        'exo_name': 'strategy_270225',
        'opt_params': [
            # OptParam(name, default_value, min_value, max_value, step)
            OptParamArray('Direction', [-1]),
            OptParam('BoxSize', 1, 50, 200, 50),
            OptParam('Reversal', 2, 2, 10, 1),
            OptParamArray('MaxMinWindowPercent', [0.05]),
            OptParam('ColumnConsecMoveCount', 2, 1, 1, 1),
            OptParamArray('RulesIndex', np.arange(9)),
            OptParam('MedianPeriod', 5, 5, 50, 10),
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