import unittest
import pandas as pd
import numpy as np

from backtester.swarms.manager import SwarmManager
from backtester.swarms.swarm import Swarm

from backtester.strategy import StrategyBase, OptParam, OptParamArray
from backtester.swarms.manager import SwarmManager
from backtester.swarms.ranking import SwarmRanker
from backtester.swarms.rebalancing import SwarmRebalance
from backtester.swarms.filters import SwarmFilter
from backtester.costs import CostsManagerEXOFixed
from backtester.swarms.rankingclasses import *

from strategies.strategy_macross_with_trail import StrategyMACrossTrail

class BacktesterTestCase(unittest.TestCase):
    def test_compare_swarm_results(self):
        STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': 'strategy_270225',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 2,
                'ranking_function': SwarmRanker.highestreturns_14days,
                'ranking_params': {
                    # 'ranking_type' - global ranking mode
                    # 'returns' - main ranking function based on highest returns N days
                    # 'relstr' - relative strength (equity / MA(equity))
                    'ranking_type': 'returns',

                    # Used for 'ranking_type' = 'relstr'
                    'ranking_relstr_ma_period': 90,
                    'ranking_relstr_upperbound': 1.4,
                    'ranking_relstr_lowerbound': 0.98,

                    # Used for 'ranking_type' = 'returns'
                    # Ranking function exta parameters (main ranking metric period)
                    'ranking_returns_period': 14,

                    # Ignoring all members which equity less than it's MovingAverage({ignore_eqty_less_ma_period})
                    # 'ignore_eqty_less_ma': True,                    # Comment the line to turn off
                    'ignore_eqty_less_ma_period': 90,  # Equity Moving Average period

                    # Ignoring all members which equity less than TOP swarmmembers quantile
                    # 'ignore_eqty_less_top_quantile': True,          # Comment the line to turn off
                    'ignore_eqty_less_top_quantile_threshold': 0.9,  # Ignore all members less than 0.9 quantile

                    # Ignoring all swarm members wich have negative MA slope
                    # 'ignore_eqty_with_negative_ma_slope': True,     # Comment the line to turn off
                    'ignore_eqty_with_negative_ma_period': 90,  # Period of moving average
                    'ignore_eqty_with_negative_ma_slope_period': 5,
                # Slope lookback filter = MA-MA[-slope_lookback] <= 0

                    # Ignoring all swarm members when the change of AvgSwarm equity is negative
                    # 'ignore_if_avg_swarm_negative_change': True,      # Comment the line to turn off
                    'ignore_if_avg_swarm_negative_change_period': 14,  # AvgSwarm change period

                },
                'rebalance_time_function': SwarmRebalance.every_friday,
                # SwarmFilter.swingpoint_daily - original TMQR Swingpoint logics from Matlab
                # SwarmFilter.volatility_chandelier - Alex's volatility based logic (old name: SwarmFilter.swingpoint_threshold)
            },
        }

        smgr = SwarmManager(STRATEGY_CONTEXT)
        smgr.run_swarm()

        STRATEGY_CONTEXT2 = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': 'strategy_270225',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 2,
                'ranking_class': RankerHighestReturns(return_period=14),
                'rebalance_time_function': SwarmRebalance.every_friday,
            },
        }

        swm = Swarm(STRATEGY_CONTEXT2)
        swm.run_swarm()

        swm.pick()

        self.assertEqual(np.all(smgr.swarm.values == swm._swarm.values), True)
        self.assertEqual(np.all(smgr.swarm_inposition.values == swm._swarm_inposition.values), True)


    def test_pick_equity_calculation(self):


        def reblance_every_5th(swarm):
            return pd.Series(swarm.index % 5 == 0, index=swarm.index)

        STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': 'strategy_270225',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 1,
                'ranking_class': RankerHighestReturns(return_period=1),
                'rebalance_time_function': reblance_every_5th
            }
        }
        swm_index = np.array(range(20))
        swm_values = np.array([
           [ 0.,  0.], # 0
           [ 1.,  -1.],
           [ 2.,  -2.],
           [ 3.,  -3.],
           [ 4.,  -4.],
           [ 5.,  -5.], # 5
           [ 6.,  -6.],
           [ 7.,  -7.],
           [ 8.,  -8.],
           [ 9.,  -9.],
           [ 6.,  -6.], # 10
           [ 5.,  -5.],
           [ 4.,  -4.],
           [ 3.,  -3.],
           [ 2.,  -2.],
           [ 1.,  -1.],   #15
           [ 0.,  0.],
           [ -1.,  1.],
           [ -2.,  2.],
           [ -3.,  3.]])

        swm = Swarm(STRATEGY_CONTEXT)
        swm._swarm = pd.DataFrame(swm_values, swm_index)
        swm._swarm_inposition = pd.DataFrame(np.ones((20, 2)), swm_index)
        swm._swarm_exposure = pd.DataFrame(-np.ones((20, 2)), swm_index)

        swm_res = np.array([
           [ 0.], #0 - ignored by default
           [ 0.],
           [ 0.],
           [ 0.],
           [ 0.],
           [ 0.], #5 - first rebalance (pick system #0)
           [ 0.], # Apply delayed rebalance we checked rebalance on #5 but change the position at #6
           [ 1.],
           [ 2.],
           [ 3.],
           [ 0.], #10 - pick another systems (but keep prev system change to next day)
           [ -1.], # Apply delayed rebalance we checked rebalance on #10 but change the position at #11
           [ 0.],
           [ 1.],
           [ 2.],
           [ 3.], #15 - keep system #1
           [ 4.],
           [ 5.],
           [ 6.],
           [ 7.]] )

        expected = pd.DataFrame(swm_res, index=swm_index)

        swm.pick()

        for k, v in expected[0].items():
            print(k)
            self.assertEqual(k, swm.picked_swarm.index[k])
            self.assertEqual(v, swm.picked_swarm[0][k])


    def test_rebalanceinformation_before_next_day(self):

        def riseup(swarm_slice, nsystems):
            result = []
            rank_info = []

            # Calculate 14-period equity returns and sort values
            last_diff = swarm_slice.diff(periods=1).iloc[-1, :].sort_values(ascending=False)

            # Pick best nsystems
            best = last_diff[:nsystems]

            for k, v in best.items():
                if not np.isnan(v) and v > 0:
                    result.append(k)
                    rank_info.append({'rank_value': v})

            return result, rank_info

        def reblance_every_5th(swarm):
            return pd.Series(swarm.index % 5 == 0, index=swarm.index)

        STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': 'strategy_270225',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 1,
                'ranking_class': RankerHighestReturns(return_period=1),
                'rebalance_time_function': reblance_every_5th
            }
        }
        swm_index = np.array(range(11))
        swm_values = np.array([
           [ 0.,  0.], # 0
           [ 1.,  -1.],
           [ 2.,  -2.],
           [ 3.,  -3.],
           [ 4.,  -4.],
           [ 5.,  -5.], # 5
           [ 6.,  -6.],
           [ 7.,  -7.],
           [ 8.,  -8.],
           [ 9.,  -9.],
           [ 6.,  -6.], # 10
           ])

        swm = Swarm(STRATEGY_CONTEXT)
        swm._swarm = pd.DataFrame(swm_values, swm_index)
        swm._swarm_inposition = pd.DataFrame(np.ones((11, 2)), swm_index)
        swm._swarm_exposure = pd.DataFrame(-np.ones((11, 2)), swm_index)

        swm_res = np.array([
           [ 0.], #0 - ignored by default
           [ 0.],
           [ 0.],
           [ 0.],
           [ 0.],
           [ 0.], #5 - first rebalance (pick system #0)
           [ 0.], # Apply delayed rebalance we checked rebalance on #5 but change the position at #6
           [ 1.],
           [ 2.],
           [ 3.],
           [ 0.], #10 - pick another systems (but keep prev system change to next day)
        ])

        expected = pd.DataFrame(swm_res, index=swm_index)

        swm.pick()

        self.assertEqual(2, len(swm.rebalance_info))
        self.assertEqual(5, swm.rebalance_info[0]['rebalance_date'])
        self.assertEqual(10, swm.rebalance_info[1]['rebalance_date'])

        for k, v in expected[0].items():
            print(k)
            self.assertEqual(k, swm.picked_swarm.index[k])
            self.assertEqual(v, swm.picked_swarm[0][k])


    def test_laststate_update(self):


        def reblance_every_5th(swarm):
            return pd.Series(swarm.index % 5 == 0, index=swarm.index)

        STRATEGY_CONTEXT = {
            'strategy': {
                'class': StrategyMACrossTrail,
                'exo_name': 'strategy_270225',
                'direction': -1,
                'opt_params': [
                    # OptParam(name, default_value, min_value, max_value, step)
                    OptParamArray('Direction', [-1]),
                    OptParam('SlowMAPeriod', 20, 10, 40, 5),
                    OptParam('FastMAPeriod', 2, 5, 20, 5),
                    OptParam('MedianPeriod', 5, 2, 10, 1)
                ],
            },
            'swarm': {
                'members_count': 1,
                'ranking_class': RankerHighestReturns(return_period=1),
                'rebalance_time_function': reblance_every_5th
            }
        }
        swm_index = np.array(range(11))
        swm_values = np.array([
           [ 0.,  0.], # 0
           [ 1.,  -1.],
           [ 2.,  -2.],
           [ 3.,  -3.],
           [ 4.,  -4.],
           [ 5.,  -5.], # 5
           [ 6.,  -6.],
           [ 7.,  -7.],
           [ 8.,  -8.],
           [ 9.,  -9.],
           [ 6.,  -6.], # 10
           ])

        swm = Swarm(STRATEGY_CONTEXT)
        swm._swarm = pd.DataFrame(swm_values, swm_index)
        swm._swarm_inposition = pd.DataFrame(np.ones((11, 2)), swm_index)
        swm._swarm_exposure = pd.DataFrame(-np.ones((11, 2)), swm_index)

        swm_res = np.array([
            0., #0 - ignored by default
            0.,
            0.,
            0.,
            0.,
            0., #5 - first rebalance (pick system #0)
            0., # Apply delayed rebalance we checked rebalance on #5 but change the position at #6
            1.,
            2.,
            3.,
            0., #10 - pick another systems (but keep prev system change to next day)
        ])

        expected = pd.DataFrame(swm_res, index=swm_index)

        swm.pick()

        self.assertEqual(2, len(swm.rebalance_info))
        self.assertEqual(5, swm.rebalance_info[0]['rebalance_date'])
        self.assertEqual(10, swm.rebalance_info[1]['rebalance_date'])

        for k, v in expected[0].items():
            #print(k)
            self.assertEqual(k, swm.picked_swarm.index[k])
            self.assertEqual(v, swm.picked_swarm[0][k])

        self.assertEqual(swm.last_date, 10)
        self.assertEqual(swm.last_rebalance_date, 10)
        self.assertEqual(swm.last_exposure, -1)
        self.assertEqual(swm.last_members_list, [1])
        self.assertEqual(True, np.all(swm.picked_equity.values == expected[0].values))


        #
        #  DO swarm update with new quotes
        #
        swm_index = np.array(range(14))


        exo_price = np.array([
            0.,  # 0 - ignored by default
            0.,
            0.,
            0.,
            0.,
            0.,  # 5 - first rebalance (pick system #0)
            0.,  # Apply delayed rebalance we checked rebalance on #5 but change the position at #6
            1.,
            2.,
            3.,
            0.,  # 10 - pick another systems (but keep prev system change to next day)
            10., # Should be added with last exposure
            11.,
            13.
        ])

        swarm_exposure = np.array([
            0.,  # 0 - ignored by default
            0.,
            0.,
            0.,
            0.,
            0.,  # 5 - first rebalance (pick system #0)
            0.,
            0.,
            0.,
            0.,
            0.,  # 10
            2.,  # Should be added with last exposure
            2.,
            2.,
        ])

        #swm = Swarm(STRATEGY_CONTEXT)
        # Little hack
        swm._last_exoquote = 0.0 # exo_price on #10
        self.assertEqual(swm.last_date, 10)
        self.assertEqual(swm.last_rebalance_date, 10)
        self.assertEqual(swm.last_exposure, -1)
        self.assertEqual(swm.last_exoquote, 0)
        self.assertEqual(swm.last_members_list, [1])

        swm.laststate_update(pd.Series(exo_price, index=swm_index), pd.Series(swarm_exposure, index=swm_index))

        self.assertEqual(swm.last_date, 13)
        self.assertEqual(swm.last_rebalance_date, 10)
        self.assertEqual(swm.last_exposure, 2)
        self.assertEqual(swm.last_exoquote, 13)
        self.assertEqual(swm.last_members_list, [1])

        swm_res = np.array([
            0.,  # 0 - ignored by default
            0.,
            0.,
            0.,
            0.,
            0.,  # 5 - first rebalance (pick system #0)
            0.,  # Apply delayed rebalance we checked rebalance on #5 but change the position at #6
            1.,
            2.,
            3.,
            0.,  # 10 - pick another systems (but keep prev system change to next day)
            -10.,  # Apply delayed rebalance we checked rebalance on #10 but change the position at #11
            -8.,
            -4.,
            ])
        expected = pd.Series(swm_res, index=swm_index)

        self.assertEqual(len(swm.picked_equity), len(expected))
        for k, v in expected.items():
            print(k)
            self.assertEqual(k, swm.picked_equity.index[k])
            self.assertEqual(v, swm.picked_equity.values[k])


