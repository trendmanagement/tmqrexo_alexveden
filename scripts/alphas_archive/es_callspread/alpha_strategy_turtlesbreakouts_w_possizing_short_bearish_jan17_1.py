#
#
#  Automatically generated file 
#        Created at: 2017-01-25 16:35:59.837790
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParam
from strategies.strategy_turtlesbreakouts_possizing import Strategy_TurtlesBreakouts_w_PosSizing
from backtester.costs import CostsManagerEXOFixed
from backtester.strategy import OptParamArray


STRATEGY_NAME = Strategy_TurtlesBreakouts_w_PosSizing.name

STRATEGY_SUFFIX = "_Bearish_Jan17_1"

STRATEGY_CONTEXT = {
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
    },
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=0.5),
        'members_count': 1,
    },
    'strategy': {
        'exo_name': 'ES_CallSpread',
        'class': Strategy_TurtlesBreakouts_w_PosSizing,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('ATR period', 1, 10, 16, 1), 
            OptParam('Rolling min max period', 1, 7, 12, 1), 
            OptParamArray('Rules index', [1]), 
        ],
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