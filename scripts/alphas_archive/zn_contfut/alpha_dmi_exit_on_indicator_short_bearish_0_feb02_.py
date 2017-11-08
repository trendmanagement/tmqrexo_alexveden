#
#
#  Automatically generated file 
#        Created at: 2017-02-08 17:34:30.580339
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_dmi_exits_on_indicator import Strategy_DMI_exit_on_indicator_events
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam


STRATEGY_NAME = Strategy_DMI_exit_on_indicator_events.name

STRATEGY_SUFFIX = "_Bearish_0_Feb02_"

STRATEGY_CONTEXT = {
    'strategy': {
        'exo_name': 'ZN_ContFut',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('DMI(DI EMAs and ATR) period', 1, 13, 23, 10), 
            OptParamArray('Rules index', [0]), 
        ],
        'class': Strategy_DMI_exit_on_indicator_events,
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
        'members_count': 1,
    },
}
