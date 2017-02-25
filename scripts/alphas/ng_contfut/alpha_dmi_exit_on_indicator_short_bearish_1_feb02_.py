#
#
#  Automatically generated file 
#        Created at: 2017-02-08 17:22:28.206042
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from strategies.strategy_dmi_exits_on_indicator import Strategy_DMI_exit_on_indicator_events
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray


STRATEGY_NAME = Strategy_DMI_exit_on_indicator_events.name

STRATEGY_SUFFIX = "_Bearish_1_Feb02_"

STRATEGY_CONTEXT = {
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'members_count': 1,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'class': Strategy_DMI_exit_on_indicator_events,
        'exo_name': 'NG_ContFut',
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('DMI(DI EMAs and ATR) period', 1, 12, 21, 1), 
            OptParamArray('Rules index', [1]), 
        ],
    },
}
