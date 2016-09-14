import unittest

import unittest
from backtester.swarms.manager import SwarmManager
import pandas as pd
import numpy as np
from backtester import matlab, backtester
from backtester.analysis import *
from backtester.strategy import StrategyBase, OptParam, OptParamArray
from backtester.swarms.manager import SwarmManager
from backtester.swarms.ranking import SwarmRanker
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.filters import SwarmFilter
from backtester.costs import CostsManagerEXOFixed
import numpy as np
from copy import deepcopy

from backtester.strategy import StrategyBase



class StrategyBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.context_nocosts = {
            'strategy': {
                'class': StrategyBase,
                'exo_name': 'strategy_270225',
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [1]),
                    OptParam('SlowMAPeriod', 20, 10, 70, 10),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 20, 4)
                ],
            },
        }

        self.context_withcosts = {
            'strategy': {
                'class': StrategyBase,
                'exo_name': 'strategy_270225',
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [1]),
                    OptParam('SlowMAPeriod', 20, 10, 70, 10),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 20, 4)
                ],
            },
            'costs': {
                'manager': CostsManagerEXOFixed,
                'context': {
                    'costs_options': 3.0,
                    'costs_futures': 3.0,
                }
            }
        }

    def test_init(self):
        s = StrategyBase(self.context_nocosts)
        self.assertEqual(s.name, 'BaseStrategy')
        self.assertEqual(s.opts, None)
        self.assertEqual(s.costs, None)

        self.assertEqual(s.context, self.context_nocosts)
        self.assertEqual(s.exo_name, 'strategy_270225')
        self.assertEqual(s.exoinfo.exo_info['name'], 'EP_BearishCollarBrokenWing')

        self.assertEqual(s.global_filter, None)
        self.assertEqual(s.global_filter_data, None)
        self.assertEqual(s._filtered_swarm, None)
        self.assertEqual(s._filtered_swarm_equity, None)


    def test_check_context(self):
        s = StrategyBase(self.context_nocosts)

        s.check_context(self.context_nocosts)

        ctx = deepcopy(self.context_nocosts)
        del ctx['strategy']
        self.assertRaises(KeyError, s.check_context, ctx)

        ctx = deepcopy(self.context_nocosts)
        del ctx['strategy']['exo_name']
        self.assertRaises(KeyError, s.check_context, ctx)

        ctx = deepcopy(self.context_nocosts)
        del ctx['strategy']['class']
        self.assertRaises(KeyError, s.check_context, ctx)

        ctx = deepcopy(self.context_nocosts)
        del ctx['strategy']['opt_params']
        self.assertRaises(KeyError, s.check_context, ctx)

        ctx = deepcopy(self.context_withcosts)
        del ctx['costs']['manager']
        self.assertRaises(KeyError, s.check_context, ctx)


    def test_slice_opts_default(self):
        ctx = deepcopy(self.context_withcosts)
        ctx['strategy']['opt_params'] =  [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [1, -1]),
                    OptParamArray('Opt2', [3, 5]),
                ]
        s = StrategyBase(ctx)
        res = s.slice_opts()
        res_required = [(1,3),(1,5),(-1,3), (-1,5)]

        self.assertEqual(len(list(res)), len(res_required))
        for i in res:
            for j in res_required:
                self.assertEqual(i, j)

    def test_slice_opts_preset(self):
        ctx = deepcopy(self.context_withcosts)
        ctx['strategy']['opt_params'] =  [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [1, -1]),
                    OptParamArray('Opt2', [3, 5]),
                ]

        ctx['strategy']['opt_preset'] = [
            # OptParam(name, default_value, min_value, max_value, step)
            (1, 5),
            (-1, 3)
        ]
        s = StrategyBase(ctx)
        res = s.slice_opts()
        res_required = [(1, 5), (-1, 3)]

        self.assertEqual(res, res_required)


if __name__ == '__main__':
    unittest.main()
