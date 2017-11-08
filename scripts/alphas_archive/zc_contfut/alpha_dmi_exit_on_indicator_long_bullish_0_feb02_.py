#
#
#  Automatically generated file 
#        Created at: 2017-02-08 10:48:18.314978
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from strategies.strategy_dmi_exits_on_indicator import Strategy_DMI_exit_on_indicator_events
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParam
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = Strategy_DMI_exit_on_indicator_events.name

STRATEGY_SUFFIX = "_Bullish_0_Feb02_"

STRATEGY_CONTEXT = {
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('DMI(DI EMAs and ATR) period', 1, 1, 4, 1), 
            OptParamArray('Rules index', [1]), 
        ],
        'class': Strategy_DMI_exit_on_indicator_events,
        'exo_name': 'ZC_ContFut',
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'costs': {
        'context': {
            'costs_futures': 3.0,
            'costs_options': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
}
