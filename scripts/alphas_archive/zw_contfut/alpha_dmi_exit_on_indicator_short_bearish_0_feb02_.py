#
#
#  Automatically generated file 
#        Created at: 2017-02-08 17:48:11.423277
#
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from strategies.strategy_dmi_exits_on_indicator import Strategy_DMI_exit_on_indicator_events


STRATEGY_NAME = Strategy_DMI_exit_on_indicator_events.name

STRATEGY_SUFFIX = "_Bearish_0_Feb02_"

STRATEGY_CONTEXT = {
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'strategy': {
        'class': Strategy_DMI_exit_on_indicator_events,
        'exo_name': 'ZW_ContFut',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('DMI(DI EMAs and ATR) period', 1, 20, 40, 5), 
            OptParamArray('Rules index', [0]), 
        ],
    },
}
