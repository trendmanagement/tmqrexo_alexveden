#
#
#  Automatically generated file 
#        Created at: 2017-01-25 16:20:50.140447
#
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray
from backtester.swarms.rebalancing import SwarmRebalance
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bullish_Jan17_0"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'swarm': {
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
        'members_count': 1,
        'rebalance_time_function': SwarmRebalance.every_friday,
    },
    'strategy': {
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
        'opt_params': [
            OptParamArray('Direction', [1]), 
            OptParam('ATR period', 1, 2, 13, 1), 
            OptParam('Rolling min max period', 1, 10, 15, 1), 
            OptParamArray('Rules index', [0]), 
        ],
        'exo_name': 'ES_CallSpread',
    },
}

if __name__ == '__main__':
    from backtester.reports.alpha_sanity_checks import AlphaSanityChecker
    from scripts.settings import *
    from exobuilder.data.exostorage import EXOStorage
    from backtester.swarms.swarm import Swarm

    storage = EXOStorage(MONGO_CONNSTR, MONGO_EXO_DB)
    STRATEGY_CONTEXT['strategy']['exo_storage'] = storage

    smgr = Swarm(STRATEGY_CONTEXT)
    smgr.run_swarm()

    asc = AlphaSanityChecker(smgr, day_step=5)
    asc.run()