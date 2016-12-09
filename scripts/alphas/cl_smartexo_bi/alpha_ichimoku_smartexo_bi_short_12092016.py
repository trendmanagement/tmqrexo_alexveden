from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam, OptParamArray
from backtester.swarms.rankingclasses import *
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_ichimokucloud import StrategyIchimokuCloud

STRATEGY_NAME = StrategyIchimokuCloud.name

STRATEGY_SUFFIX = 'ichimoku-short-12092016'

STRATEGY_CONTEXT = {
    'strategy': {
        'class': StrategyIchimokuCloud,
        'exo_name': 'CL_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',        # <---- Select and paste EXO name from cell above
        'opt_params': [
                        #OptParam(name, default_value, min_value, max_value, step)
                        OptParamArray('Direction', [-1]),
                        OptParam('conversion_line_period', 9, 2, 17, 5),
                        OptParam('base_line_period', 26, 13, 26, 13),
                        OptParam('leading_spans_lookahead_period', 26, 26, 26, 1),
                        OptParam('leading_span_b_period', 52, 5, 5, 5),
                        #OptParamArray('RulesIndex', np.arange(14)),
                        OptParamArray('RulesIndex', [11]),
                        OptParam('MedianPeriod', 5, 10, 60, 50)
            ],
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,

    },
    'costs':{
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        }
    }
}