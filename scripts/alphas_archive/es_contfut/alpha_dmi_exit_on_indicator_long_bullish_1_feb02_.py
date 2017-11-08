#
#
#  Automatically generated file 
#        Created at: 2017-02-08 12:40:42.706232
#
from strategies.strategy_dmi_exits_on_indicator import Strategy_DMI_exit_on_indicator_events
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = Strategy_DMI_exit_on_indicator_events.name

STRATEGY_SUFFIX = "_Bullish_1_Feb02_"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'strategy': {
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('DMI(DI EMAs and ATR) period', 1, 3, 7, 1), 
            OptParamArray('Rules index', [1]), 
        ],
        'class': Strategy_DMI_exit_on_indicator_events,
        'exo_name': 'ES_ContFut',
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
}
