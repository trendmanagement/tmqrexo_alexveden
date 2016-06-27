import sys,os
sys.path.append('..')
sys.path.append('../..')
from backtester import matlab, backtester
from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam, OptParamArray
from backtester.swarms.manager import SwarmManager
from backtester.swarms.ranking import SwarmRanker
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.filters import SwarmFilter
from backtester.costs import CostsManagerEXOFixed
from backtester.exoinfo import EXOInfo

from backtester.positionsizing import PositionSizingBase
import pandas as pd
import numpy as np
import scipy
import os, sys

from strategies.strategy_swingpoint import StrategySwingPoint
from strategies.strategy_macross_with_trail import StrategyMACrossTrail
try:
    from .settings import *
except SystemError:
    from settings import *

if __name__ == '__main__':
    for f in os.listdir(sys.argv[1]):
        if 'strategy_' not in f:
            continue
        exo_name = os.path.join(sys.argv[1], f)
        print("Processing "+exo_name)
        for name, swarm_context in BATCH_CONTEXT.items():
            print("Running swarm " + name)

            STRATEGY_CONTEXT_COMMON.update(swarm_context)
            STRATEGY_CONTEXT_COMMON['strategy']['exo_name'] = exo_name
            STRATEGY_CONTEXT_COMMON['strategy']['suffix'] = name

            smgr = SwarmManager(STRATEGY_CONTEXT_COMMON)
            smgr.run_swarm()
            smgr.pick()

            # Saving results to swarms directory
            smgr.save('./swarms/')

    print('Done')
