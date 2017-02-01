#
#
#  Automatically generated file 
#        Created at: 2017-01-25 20:01:10.599728
#
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.strategy import OptParam
from backtester.swarms.rankingclasses import RankerBestWithCorrel
from backtester.strategy import OptParamArray
from backtester.costs import CostsManagerEXOFixed
from strategies.strategy_swingpoint import StrategySwingPoint


STRATEGY_NAME = StrategySwingPoint.name

STRATEGY_SUFFIX = "_Bi_Jan17_"

STRATEGY_CONTEXT = {
    'swarm': {
        'rebalance_time_function': SwarmRebalance.every_friday,
        'ranking_class': RankerBestWithCorrel(window_size=-1, correl_threshold=-0.5),
        'members_count': 1,
    },
    'strategy': {
        'exo_name': 'ES_SmartEXO_Ichi_DeltaTargeting_Dec3_Bi_Spread',
        'class': StrategySwingPoint,
        'opt_params': [
            OptParamArray('Direction', [-1]), 
            OptParam('sphTreshold', 2, 4, 5, 1), 
            OptParam('splTreshold', 2, 1, 2, 1), 
            OptParamArray('RulesIndex', [2]), 
            OptParam('MedianPeriod', 5, 32, 68, 13), 
        ],
    },
    'costs': {
        'manager': CostsManagerEXOFixed,
        'context': {
            'costs_options': 3.0,
            'costs_futures': 3.0,
        },
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