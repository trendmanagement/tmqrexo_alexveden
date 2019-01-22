#
#
#  Automatically generated file 
#        Created at: 2017-02-08 17:36:08.459763
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_dmi_exits_on_indicator import Strategy_DMI_exit_on_indicator_events
from backtester.strategy import OptParam
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed


STRATEGY_NAME = Strategy_DMI_exit_on_indicator_events.name

STRATEGY_SUFFIX = "_Bullish_1_Feb02_"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('DMI(DI EMAs and ATR) period', 1, 3, 7, 1), 
            OptParamArray('Rules index', [1]), 
        ],
        'exo_name': 'ZN_ContFut',
        'class': Strategy_DMI_exit_on_indicator_events,
    },
}
