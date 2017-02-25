#
#
#  Automatically generated file 
#        Created at: 2017-02-08 17:19:39.424358
#
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray
from backtester.strategy import OptParam
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_dmi_exits_on_indicator import Strategy_DMI_exit_on_indicator_events
from backtester.swarms.rebalancing import SwarmRebalance


STRATEGY_NAME = Strategy_DMI_exit_on_indicator_events.name

STRATEGY_SUFFIX = "_Bullish_1_Feb02_"

STRATEGY_CONTEXT = {
    'strategy': {
        'class': Strategy_DMI_exit_on_indicator_events,
        'exo_name': 'NG_ContFut',
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('DMI(DI EMAs and ATR) period', 1, 158, 230, 20), 
            OptParamArray('Rules index', [1]), 
        ],
    },
    'costs': {
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
        'manager': CostsManagerEXOFixed,
    },
    'swarm': {
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
    },
}
